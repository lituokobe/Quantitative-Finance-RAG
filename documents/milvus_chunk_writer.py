from typing import Any, Callable
import uuid
import time
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection, Function, FunctionType
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
    Supports Hybrid Search (Dense + Sparse BM25).

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
        self.alias = alias # one alias can have one connection with the collection
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
        if connections.has_connection(self.alias): # If the connection with this collection already exists under the alias
            return

        connections.connect(
            alias=self.alias,
            host=self.host,
            port=self.port,
        )

    # --------------------------------------------------
    # Collection + schema
    # --------------------------------------------------
    def _wait_for_collection(self, timeout: int = 30):
        start = time.time()
        while time.time() - start < timeout:
            if utility.has_collection(self.collection_name, using=self.alias): # use utility to check if the collection exists without load it
                return
            time.sleep(0.2)
        raise TimeoutError(f"Collection {self.collection_name} not found after {timeout}s")

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
            FieldSchema(name="dense", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
            # 'text' is the input for the BM25 function
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535, enable_analyzer=True),
            # 'sparse' is the output of the BM25 function
            FieldSchema(name="sparse", dtype=DataType.SPARSE_FLOAT_VECTOR),

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
            description="Finance RAG chunks (dense + sparse)",
        )

        # Define BM25 function
        bm25_function = Function(
            name = "text_bm25_emb",
            input_field_names=['text'],
            output_field_names=['sparse'],
            function_type=FunctionType.BM25
        )
        schema.add_function(bm25_function)

        # Create the collection (this registers it in Milvus)
        Collection(name=self.collection_name, schema=schema, using=self.alias)
        self._wait_for_collection() # Wait until Milvus acknowledges it exists with defensive wait loop

        # Re-instantiate the Collection object and store it
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
        Create both dense and sparse indexes only if missing.
        """
        assert self._collection is not None

        # Dense Index
        if not self._collection.has_index(index_name="dense_index"):
            self._collection.create_index(
                field_name="dense",
                index_name="dense_index",
                index_params={
                    "index_type": "HNSW", # a fast graph-based ANN index for dense embeddings
                    "metric_type": self.metric_type,
                    "params": {
                        "M": 16,
                        "efConstruction": 200,
                    },
                },
            )
        # Sparse Index
        if not self._collection.has_index(index_name="sparse_index"):
            self._collection.create_index(
                field_name="sparse",
                index_name="sparse_index",
                index_params={
                    "index_type": "SPARSE_INVERTED_INDEX", # Milvus built-in index type for sparse vector search
                    "metric_type": self.metric_type, #BM25 also use IP
                    "params": {
                        "drop_ratio_build": 0.2,# drops the lowest 20% of weights
                        # before building the inverted index. Reduces index size and memory usage. Slight loss in recall (you’re discarding weak signals).
                        "inverted_index_algo": "DAAT_MAXSCORE", # Uses upper-bound pruning to skip low-scoring docs early, faster for top-K retrieval
                    }
                },
            )

    # --------------------------------------------------
    # Insert documents
    # --------------------------------------------------
    def add_documents(self, docs: list[Any]) -> int:
        """
        Insert a batch of LangChain Document objects. Milvus Function automatically handles the 'sparse' field.

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
        texts = [(d.page_content or "")[:65535] for d in docs] # defensive take first 65535 avoid exceeding te limit of 'text' field

        # ---- embeddings (batch) ----
        embeddings = self.embedding_fn(texts)
        if embeddings is None or len(embeddings) == 0:
            raise ValueError("Embedding function returned empty list")

        if len(embeddings) != len(texts):
            raise ValueError("Embedding count mismatch")

        for e in embeddings:
            if len(e) != self.dim:
                raise ValueError(
                    f"Embedding dimension mismatch: expected {self.dim}, got {len(e)}"
                )

        ids = [str(uuid.uuid4()) for _ in docs] #uuid is not deterministic

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

        # Do not pass 'sparse' data here.
        # The Schema Function generates it from 'texts' automatically.
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