from langchain_core.documents import Document
from langchain_milvus import Milvus, BM25BuiltInFunction
from pymilvus import IndexType, MilvusClient, Function
from pymilvus.client.types import MetricType, DataType, FunctionType

from config.paths import MILVUS_URI
from config.rag_config import COLLECTION_NAME
from models.models import qwen3_embedding_model
from utils.log_utils import log

class MilvusVectorSave:
    def __init__(self):
        self.vector_store_saved: Milvus | None = None

    def create_collection(self):
        client = MilvusClient(uri=MILVUS_URI)

        # ----- Schema Definition -----
        schema = client.create_schema()
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
        schema.add_field(field_name="text",
                         datatype=DataType.VARCHAR,
                         max_length=65535,
                         enable_analyzer=True,
                         analyzer_params={"type": "standard"})
        schema.add_field(field_name="category", datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name="source", datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name="filename", datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name="title", datatype=DataType.VARCHAR, max_length=1000)
        schema.add_field(field_name="breadcrumb", datatype=DataType.VARCHAR, max_length=2000)
        schema.add_field(field_name="section_level", datatype=DataType.INT64)
        schema.add_field(field_name="contains_math", datatype=DataType.BOOL)
        schema.add_field(field_name="contains_table", datatype=DataType.BOOL)
        # schema.add_field(field_name="sparse", datatype=DataType.SPARSE_FLOAT_VECTOR, nullable=True)
        schema.add_field(field_name="dense", datatype=DataType.FLOAT_VECTOR, dim=1024, nullable=True)

        # Prepare vector field
        # bm25_func = Function(
        #     name="text_bm25_emb",
        #     function_type=FunctionType.BM25,
        #     input_field_names=["text"],
        #     output_field_names=["sparse"]
        # )
        # schema.add_function(bm25_func)

        # ----- Indexes -----
        index_params = client.prepare_index_params()
        # index_params.add_index(  # index for sparse
        #     field_name="sparse",
        #     index_name="sparse_inverted_index",
        #     index_type="SPARSE_INVERTED_INDEX",  # Inverted index type for sparse vectors
        #     metric_type=MetricType.IP,
        #     params={
        #         "inverted_index_algo": "DAAT_MAXSCORE",
        #         "bm25_k1": 1.2,
        #         "bm25_b": 0.75
        #     },
        # )
        index_params.add_index(  # index for dense
            field_name="dense",
            index_name="dense_inverted_index",
            index_type=IndexType.HNSW,  # Inverted index type for sparse vectors
            metric_type=MetricType.IP,
            params={"M": 16, "efConstruction": 64}  # M: count of near node to connect, efConstruction: search scope
        )
        if COLLECTION_NAME in client.list_collections():
            client.release_collection(collection_name=COLLECTION_NAME)
            client.drop_index(collection_name=COLLECTION_NAME, index_name='sparse_inverted_index')
            client.drop_index(collection_name=COLLECTION_NAME, index_name='dense_inverted_index')
            client.drop_collection(collection_name=COLLECTION_NAME)

        client.create_collection(
            collection_name=COLLECTION_NAME,
            schema=schema,
            index_params=index_params
        )
        log.info(f"Successfully created collection: {COLLECTION_NAME}")

    def create_connection(self):
        """
        create a connection: milvus + langchain
        :return:
        """

        self.vector_store_saved = Milvus(#This milvus instance is from langchain_milvus
            #Milvus is an unstructured database, meaning the fields of the data are not necessarily consistent
            #Here, we only have 2 keys added to the vector: dense, sparse
            #other keys will be added on the go if there are other keys in the data or metadata
            embedding_function=qwen3_embedding_model, #dense vector
            collection_name=COLLECTION_NAME,
            # builtin_function=BM25BuiltInFunction(), #sparse vector
            vector_field="dense",#['dense', 'sparse'],
            consistency_level="Strong", #highest level of consistency: Strong > Session > Bounded > Eventually
            auto_id=True,
            connection_args={"uri": MILVUS_URI},
        )

    def add_documents(self, datas: list[Document]):
        if not datas:
            return
        self.vector_store_saved.add_documents(datas)

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
