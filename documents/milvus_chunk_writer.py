from typing import Any, Callable
import uuid
import time

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

from utils.log_utils import log


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def _clip(value: Any, max_len: int) -> str:
    """
    Safely convert to string and clip to max_len.
    Prevents Milvus VARCHAR overflow errors.
    """
    return str(value or "")[:max_len]


# --------------------------------------------------
# Milvus Writer
# --------------------------------------------------
class MilvusChunkWriter:
    """
    Production-grade Milvus writer for FinanceMarkdownParser outputs.

    Dense-vector RAG ingestion with:
    - schema stability
    - batch embeddings
    - explicit indexing
    - crash-safe flushing
    """

    def __init__(
        self,
        collection_name: str,
        embedding_fn: Callable[[list[str]], list[list[float]]],
        dim: int,
        host: str = "localhost",
        port: str = "19530",
        metric_type: str = "IP",
        alias: str = "default",
        flush_every: int = 10,  # flush every N batches
    ):
        if embedding_fn is None:
            raise ValueError("embedding_fn must be provided")

        self.collection_name = collection_name
        self.embedding_fn = embedding_fn
        self.dim = dim
        self.host = host
        self.port = port
        self.metric_type = metric_type
        self.alias = alias
        self.flush_every = flush_every

        self._collection: Collection | None = None
        self._insert_batches = 0

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------
    def connect(self):
        """
        Idempotent Milvus connection.
        Safe under retries and multi-process execution.
        """
        if connections.has_connection(self.alias):
            return

        connections.connect(
            alias=self.alias,
            host=self.host,
            port=self.port,
        )

    # --------------------------------------------------
    # Collection + schema
    # --------------------------------------------------
    def create_collection(self, recreate: bool = False):
        """
        Ensure collection exists.
        Optionally drop & recreate.
        """
        self.connect()

        if utility.has_collection(self.collection_name, using=self.alias):
            if not recreate:
                self._collection = Collection(self.collection_name, using=self.alias)
                return
            Collection(self.collection_name, using=self.alias).drop()

        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),

            # ---- metadata ----
            FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=1024),
            FieldSchema(name="breadcrumb", dtype=DataType.VARCHAR, max_length=2048),
            FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=1024),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=1024),
            FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="block_type", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="section_level", dtype=DataType.INT64),
            FieldSchema(name="contains_math", dtype=DataType.BOOL),
            FieldSchema(name="contains_table", dtype=DataType.BOOL),
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Finance RAG chunks (dense vector)",
        )

        self._collection = Collection(
            name=self.collection_name,
            schema=schema,
            using=self.alias,
        )

        self._ensure_index()

    # --------------------------------------------------
    # Indexing
    # --------------------------------------------------
    def _ensure_index(self):
        """
        Create index only if missing.
        """
        assert self._collection is not None

        if self._collection.has_index():
            return

        self._collection.create_index(
            field_name="embedding",
            index_params={
                "index_type": "HNSW",
                "metric_type": self.metric_type,
                "params": {
                    "M": 16,
                    "efConstruction": 200,
                },
            },
        )

    # --------------------------------------------------
    # Insert documents
    # --------------------------------------------------
    def add_documents(self, docs: list[Any]) -> int:
        """
        Insert a batch of LangChain Document objects.

        Returns:
            int: number of documents successfully inserted.
        """
        if not docs:
            return 0

        if self._collection is None:
            if not utility.has_collection(self.collection_name, using=self.alias):
                raise RuntimeError(
                    f"Collection '{self.collection_name}' does not exist. "
                    "Call create_collection() first."
                )
            self._collection = Collection(self.collection_name, using=self.alias)

        # ---- text ----
        texts = [(d.page_content or "")[:65535] for d in docs]

        # ---- embeddings (batch) ----
        embeddings = self.embedding_fn(texts)
        if not embeddings:
            raise ValueError("Embedding function returned empty list")

        if len(embeddings) != len(texts):
            raise ValueError("Embedding count mismatch")

        for e in embeddings:
            if len(e) != self.dim:
                raise ValueError(
                    f"Embedding dimension mismatch: expected {self.dim}, got {len(e)}"
                )

        ids = [str(uuid.uuid4()) for _ in docs]

        # ---- metadata ----
        titles, breadcrumbs, filenames = [], [], []
        sources, categories, block_types = [], [], []
        section_levels, contains_math, contains_table = [], [], []

        for d in docs:
            meta: dict[str, Any] = d.metadata or {}

            titles.append(_clip(meta.get("title"), 1024))
            breadcrumbs.append(_clip(meta.get("breadcrumb"), 2048))
            filenames.append(_clip(meta.get("filename"), 1024))
            sources.append(_clip(meta.get("source"), 1024))
            categories.append(_clip(meta.get("category"), 256))
            block_types.append(_clip(meta.get("block_type"), 256))

            section_levels.append(int(meta.get("section_level", 0) or 0))
            contains_math.append(bool(meta.get("contains_math", False)))
            contains_table.append(bool(meta.get("contains_table", False)))

        data = [
            ids,
            embeddings,
            texts,
            titles,
            breadcrumbs,
            filenames,
            sources,
            categories,
            block_types,
            section_levels,
            contains_math,
            contains_table,
        ]

        # ---- insert with simple retry ----
        for attempt in range(3):
            try:
                self._collection.insert(data)
                break
            except Exception as e:
                if attempt == 2:
                    raise
                log.error(f"[MilvusChunkWriter] Insert failed (attempt {attempt+1}), retrying: {e}")
                time.sleep(0.5)

        self._insert_batches += 1
        if self._insert_batches % self.flush_every == 0:
            self._collection.flush()

        return len(docs)

    # --------------------------------------------------
    # Finalize
    # --------------------------------------------------
    def flush(self):
        if self._collection is not None:
            self._collection.flush()