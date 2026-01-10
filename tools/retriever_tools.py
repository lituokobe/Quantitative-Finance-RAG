from langchain_core.tools import create_retriever_tool
from documents.milvus_db import MilvusVectorSave

mv = MilvusVectorSave()
mv.create_connection()
retriever = mv.vector_store_saved.as_retriever(
    search_type = "similarity",
    search_kwargs = {
        "k": 6,
        "score_threshold": 0.1, # filters out low‑quality results. Only return documents with hybrid score ≥ 0.1
        "ranker_type":"rrf", # Reciprocal Rank Fusion. This fuses Dense search results and Sparse BM25 results
        "ranker_params":{"k":100}, # RRF hyperparameter. Larger k → smoother fusion; Smaller k → more weight on top‑ranked items; k=100 is a common default.
        # "filter":{"category":"content"}, # Only search documents where metadata.category  == 'content'.”
    }
)

retriever_tool = create_retriever_tool(
    name = "retriever",
    description = "Search and return information on finance, including option calculation, quantitative finance and banking.",
    retriever = retriever
)