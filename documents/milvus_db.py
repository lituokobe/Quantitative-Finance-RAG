from langchain_core.documents import Document
from langchain_milvus import Milvus, BM25BuiltInFunction
from pymilvus import MilvusClient, DataType, Function, FunctionType, IndexType
from pymilvus.client.types import MetricType
from config.paths import MILVUS_URI
from config.rag_config import COLLECTION_NAME
from models.models import qwen3_embedding_model

class MilvusVectorSave:
    """
    Save new document data to Milvus (dense + sparse hybrid).

    - `text` is the raw content used by BM25 built-in function to create sparse vectors.
    - `dense` is populated via qwen3_embedding_model.
    - Hybrid search uses both fields through langchain_milvus.Milvus + BM25BuiltInFunction.
    """
    def __init__(self):
        self.vector_store_saved: Milvus|None = None

    def create_collection(self):
        """
        Create a new collection for hybrid search.
        """
        client  = MilvusClient(uri = MILVUS_URI) # use MilvusClient from pymilvus to create the client

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
            max_length = 2048,
            # enable_analyzer = True,
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
        schema.add_field(field_name="breadcrumb", datatype=DataType.VARCHAR, max_length=1000)
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
                "inverted_index_algo":"DAAT_MAXSCORE", # Algorithm for building and querying the index. Valid values: DAAT_MAXSCORE, DAAT_WAND, TAAT_NAIVE.
                # Query execution strategy
                # DAAT = Document-at-a-time
                # MAXSCORE = skip low-impact terms early
                # Best default for performance
                "bm25_k1":1.2,
                "bm25_b":0.75
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
                "efConstruction":64,
            }
        )

        # ----- Recreate collection if exists -----
        if COLLECTION_NAME in client.list_collections():
            client.release_collection(collection_name=COLLECTION_NAME)
            client.drop_index(collection_name=COLLECTION_NAME, index_name="sparse_inverted_index")
            client.drop_index(collection_name=COLLECTION_NAME, index_name="dense_inverted_index")
            client.drop_collection(collection_name=COLLECTION_NAME)

        client.create_collection(
            collection_name=COLLECTION_NAME,
            schema=schema,
            index_params=index_params
        )

    def create_connection(self):
        """
        Create a connection: Milvus + LangChain/LangGraph
        Use Milvus fro LangChian-Milvus to connect and retrieve
        """
        self.vector_store_saved = Milvus(
            embedding_function=qwen3_embedding_model,
            collection_name=COLLECTION_NAME,
            builtin_function=BM25BuiltInFunction(),
            vector_field = ["dense", "sparse"],
            consistency_level="Strong",  # highest level of consistency: Strong > Session > Bounded > Eventually
            auto_id = True,
            connection_args = {"uri":MILVUS_URI}
        )

    def add_documents(self, datas: list[Document]):
        self.vector_store_saved.add_documents(documents=datas)