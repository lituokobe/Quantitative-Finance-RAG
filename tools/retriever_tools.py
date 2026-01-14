from langchain_core.tools import create_retriever_tool
from documents.milvus_db import MilvusVectorSave
from utils.log_utils import log

def create_hybrid_retriever_tool(
        k: int = 9,
        score_threshold: float = 0.1,
        ranker_type: str = "rrf",
        ranker_params: dict | None = None,
        filter_dict: dict | None = None,
        name: str = "retriever",
        description: str = "Search and return information on finance, including option calculation, quantitative finance and banking."
):
    """
    Create a hybrid search retriever tool (dense + sparse BM25).

    Args:
        k: Number of documents to retrieve
        score_threshold: Minimum hybrid score threshold (0.0-1.0)
        ranker_type: "rrf" (Reciprocal Rank Fusion) or "weighted"
        ranker_params: RRF parameters, e.g., {"k": 100}
        filter_dict: Metadata filter, e.g., {"category": "content"}
        name: Tool name for agent
        description: Tool description for agent

    Returns:
        LangChain retriever tool
    """
    if ranker_params is None:
        ranker_params = {"k": 100}

    # Initialize Milvus connection
    mv = MilvusVectorSave()
    mv.create_connection()

    # Get hybrid retriever
    retriever = mv.get_retriever(
        search_type="similarity",
        k=k,
        score_threshold=score_threshold,
        ranker_type=ranker_type,
        ranker_params=ranker_params,
        filter_dict=filter_dict
    )

    # Create tool
    r_tool = create_retriever_tool(
        name=name,
        description=description,
        retriever=retriever
    )

    log.info(f"Created hybrid retriever tool '{name}' with k={k}, threshold={score_threshold}")

    return r_tool


# Default tool for backward compatibility
def get_default_retriever_tool():
    """Get the default hybrid retriever tool with standard parameters."""
    return create_hybrid_retriever_tool(
        k=9,
        score_threshold=0.1, # filters out low‑quality results. Only return documents with hybrid score ≥ 0.1
        ranker_type="rrf", # Reciprocal Rank Fusion. This fuses Dense search results and Sparse BM25 results
        ranker_params={"k": 100} # RRF hyperparameter. Larger k → smoother fusion; Smaller k → more weight on top‑ranked items; k=100 is a common default.
    )

# Pre-configured tool instances for common use cases
def get_high_recall_tool():
    """High recall: more results, lower threshold."""
    return create_hybrid_retriever_tool(
        k=15,
        score_threshold=0.05,
        name="high_recall_retriever",
        description="Comprehensive search for finance information with high recall."
    )


def get_high_precision_tool():
    """High precision: fewer results, higher threshold."""
    return create_hybrid_retriever_tool(
        k=5,
        score_threshold=0.3,
        name="high_precision_retriever",
        description="Precise search for finance information with high confidence threshold."
    )


def get_math_focused_tool():
    """Tool focused on mathematical content."""
    return create_hybrid_retriever_tool(
        k=9,
        score_threshold=0.1,
        filter_dict={"contains_math": True},
        name="math_retriever",
        description="Search finance documents containing mathematical formulas and equations."
    )


def get_table_focused_tool():
    """Tool focused on tabular data."""
    return create_hybrid_retriever_tool(
        k=9,
        score_threshold=0.1,
        filter_dict={"contains_table": True},
        name="table_retriever",
        description="Search finance documents containing tables and structured data."
    )


# For backward compatibility with your existing code
retriever_tool = get_default_retriever_tool()

# Test
if __name__ == "__main__":
    """Test the hybrid retriever tool."""

    # Test 1: Default tool
    print("=" * 80)
    print("Test 1: Default Hybrid Retriever")
    print("=" * 80)

    default_tool = get_default_retriever_tool()
    results = default_tool.invoke("What is a European call option?")

    print(f"\nFound {len(results)} results:")
    for i, doc in enumerate(results[:3]):
        print(f"\n--- Result {i + 1} ---")
        print(f"Score: {doc.metadata.get('relevance_score', 'N/A')}")
        print(f"Title: {doc.metadata.get('title', 'N/A')}")
        print(f"Contains Math: {doc.metadata.get('contains_math', False)}")
        print(f"Content: {doc.page_content[:200]}...")

    # Test 2: High precision tool
    print("\n" + "=" * 80)
    print("Test 2: High Precision Retriever")
    print("=" * 80)

    precision_tool = get_high_precision_tool()
    results = precision_tool.invoke("option pricing formula")
    print(f"\nFound {len(results)} high-precision results")

    # Test 3: Math-focused tool
    print("\n" + "=" * 80)
    print("Test 3: Math-Focused Retriever")
    print("=" * 80)

    math_tool = get_math_focused_tool()
    results = math_tool.invoke("Black-Scholes formula")
    print(f"\nFound {len(results)} math-focused results")

    # Test 4: Custom configuration
    print("\n" + "=" * 80)
    print("Test 4: Custom Configuration")
    print("=" * 80)

    custom_tool = create_hybrid_retriever_tool(
        k=12,
        score_threshold=0.15,
        ranker_params={"k": 60},  # Smaller k = more weight on top results
        name="custom_retriever",
        description="Custom configured retriever"
    )
    results = custom_tool.invoke("derivative hedging strategies")
    print(f"\nFound {len(results)} results with custom config")