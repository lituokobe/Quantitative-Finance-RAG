from langchain_core.documents import Document
from langchain_milvus import Milvus, BM25BuiltInFunction
from pymilvus import MilvusClient, DataType, Function, FunctionType, IndexType
from pymilvus.client.types import MetricType
from config.paths import MILVUS_URI
from config.rag_config import COLLECTION_NAME
from models.models import qwen3_embedding_model
from utils.log_utils import log


class MilvusVectorSave:
    """
    Connects to the existing Hybrid Milvus collection for retrieval. (dense + sparse hybrid).

    - `text` is the raw content used by BM25 built-in function to create sparse vectors.
    - `dense` is populated via qwen3_embedding_model.
    - Hybrid search uses both fields through langchain_milvus.Milvus + BM25BuiltInFunction.
    """
    def __init__(self):
        self.vector_store: Milvus|None = None

    def create_collection(self, recreate:bool=False):
        """
        Create a new collection for hybrid search.
        """
        client  = MilvusClient(uri = MILVUS_URI) # use MilvusClient from pymilvus to create the client

        # ----- Check if collection exists -----
        if COLLECTION_NAME in client.list_collections():
            if recreate:
                log.info(f"Dropping existing collection: {COLLECTION_NAME}")
                client.release_collection(collection_name=COLLECTION_NAME)
                # Drop indexes first
                try:
                    client.drop_index(collection_name=COLLECTION_NAME, index_name="sparse_inverted_index")
                    client.drop_index(collection_name=COLLECTION_NAME, index_name="dense_inverted_index")
                except:
                    pass
                client.drop_collection(collection_name=COLLECTION_NAME)
            else:
                log.info(f"Collection {COLLECTION_NAME} already exists. Skipping creation.")
                return
        # ----- Schema -----
        schema = client.create_schema()
        schema.add_field(
            field_name = "id",
            datatype = DataType.INT64,
            is_primary = True,
            auto_id = True
        )
        schema.add_field(
            field_name = "text",
            datatype = DataType.VARCHAR,
            max_length = 65535,
            enable_analyzer = True,
            analyzer_params={
                "type": "standard",  # Standard tokenizer for BM25
            }
            # analyzer_params = {
            #     "tokenizer":"standard",
            #     "filter":["lowercase", "porter_stem"]
            #     # Stemming conflates word forms: run, running, runs → run
            #     # It helps recall, but lightly hurts precision
            #     # For RAG, recall > precision (LLM reranks later).
            # }
        )
        schema.add_field(field_name='category', datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name='source', datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name='filename', datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name='title', datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name="breadcrumb", datatype=DataType.VARCHAR, max_length=2000)
        schema.add_field(field_name="section_level", datatype=DataType.INT64)
        schema.add_field(field_name="contains_math", datatype=DataType.BOOL)
        schema.add_field(field_name="contains_table", datatype=DataType.BOOL)

        # Sparse + Dense vectors
        schema.add_field(
            field_name='sparse',
            datatype=DataType.SPARSE_FLOAT_VECTOR
        )
        schema.add_field(
            field_name='dense',
            datatype=DataType.FLOAT_VECTOR,
            dim=1024 #Qwen3-Embedding-0.6B embedding dimension
        )

        # ----- BM25 sparse function -----
        # Add a function (from pymilvus) using BM25 to convert text to sparse vectors
        # Dense vectors are generated outside Milvus by the embedding model
        bm25_function = Function(
            name = "text_bm25_emb",
            input_field_names = ["text"], # Name of the VARCHAR field containing raw text data
            output_field_names = ["sparse"],
            function_type = FunctionType.BM25
        )
        schema.add_function(bm25_function)

        # ----- Indexes -----
        index_params = client.prepare_index_params()

        # Dense HNSW index
        index_params.add_index(
            field_name = "sparse",
            index_name = "sparse_inverted_index",
            index_type = "SPARSE_INVERTED_INDEX",
            metric_type = MetricType.IP,
            params = {
                "drop_ratio_build": 0.2,
                "inverted_index_algo":"DAAT_MAXSCORE", # Algorithm for building and querying the index. Valid values: DAAT_MAXSCORE, DAAT_WAND, TAAT_NAIVE.
                # Query execution strategy
                # DAAT = Document-at-a-time
                # MAXSCORE = skip low-impact terms early
                # Best default for performance
                # "bm25_k1":1.2,
                # "bm25_b":0.75
            }
        )

        # Dense HNSW index
        index_params.add_index(
            field_name = "dense",
            index_name = "dense_inverted_index",
            index_type = IndexType.HNSW,
            metric_type = MetricType.IP, # When embeddings are normalized, IP means COSINE; Milvus does not have detault COSINE metric
            params = {
                "M":16,
                "efConstruction":200,
            }
        )

        client.create_collection(
            collection_name=COLLECTION_NAME,
            schema=schema,
            index_params=index_params
        )
        log.info(f"Successfully created hybrid search collection: {COLLECTION_NAME}")

    def create_connection(self):
        """
        Create a connection: Milvus + LangChain/LangGraph
        Use Milvus fro LangChian-Milvus to connect and retrieve
        """
        try:
            self.vector_store_saved = Milvus(
                embedding_function=qwen3_embedding_model,
                collection_name=COLLECTION_NAME,
                # builtin_function=BM25BuiltInFunction(),
                vector_field = "dense", #["dense", "sparse"],
                consistency_level="Strong",  # highest level of consistency: Strong > Session > Bounded > Eventually
                auto_id = True,
                connection_args = {"uri":MILVUS_URI}
            )
            log.info(f"Successfully connected to Milvus collection: {COLLECTION_NAME}")

        except Exception as e:
            log(f"Failed to connect to Milvus collection {COLLECTION_NAME}: {e}")
            raise

    def add_documents(self, datas: list[Document]):
        if self.vector_store_saved is None:
            raise RuntimeError("Must call create_connection() before adding documents")

        try:
            self.vector_store_saved.add_documents(documents=datas)
            log.info(f"Successfully added {len(datas)} documents to {COLLECTION_NAME}")
        except Exception as e:
            log.error(f"Failed to add documents: {e}")
            raise

    def get_retriever(
            self,
            search_type: str = "similarity",
            k: int = 9,
            score_threshold: float = 0.1,
            ranker_type: str = "rrf",
            ranker_params: dict | None = None,
            filter_dict: dict | None = None
    ):
        """
        Get a retriever configured for hybrid search.

        Args:
            search_type: Type of search ("similarity", "mmr", "similarity_score_threshold")
            k: Number of documents to retrieve
            score_threshold: Minimum score threshold for results
            ranker_type: Ranking algorithm ("rrf" or "weighted")
            ranker_params: Parameters for the ranker (e.g., {"k": 100} for RRF)
            filter_dict: Metadata filter (e.g., {"category": "content"})

        Returns:
            LangChain retriever configured for hybrid search
        """
        if self.vector_store_saved is None:
            raise RuntimeError("Must call create_connection() before getting retriever")

        if ranker_params is None:
            ranker_params = {"k": 100}  # Default RRF parameter

        search_kwargs = {
            "k": k,
            "score_threshold": score_threshold,
            "ranker_type": ranker_type,
            "ranker_params": ranker_params,
        }

        if filter_dict:
            search_kwargs["filter"] = filter_dict

        retriever = self.vector_store_saved.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )

        log.info(
            f"Created hybrid retriever: k={k}, ranker={ranker_type}, "
            f"threshold={score_threshold}, filter={filter_dict}"
        )

        return retriever


# Convenience function for quick setup
def get_hybrid_retriever(
        k: int = 9,
        score_threshold: float = 0.1,
        ranker_type: str = "rrf",
        filter_dict: dict | None = None
):
    """
    Quick setup for hybrid retriever.

    Usage:
        retriever = get_hybrid_retriever(k=9, score_threshold=0.1)
    """
    mv = MilvusVectorSave()
    mv.create_connection()
    return mv.get_retriever(
        k=k,
        score_threshold=score_threshold,
        ranker_type=ranker_type,
        filter_dict=filter_dict
    )