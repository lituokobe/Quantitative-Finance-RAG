import os
from langchain_core.documents import Document
from config.paths import MD_PATH
from config.rag_config import COLLECTION_NAME
from documents.md_parser import FinanceMarkdownParser
from documents.milvus_db import MilvusVectorSave
from utils.log_utils import log


def ingest_markdown_files(
        md_dir: str,
        batch_size: int = 32,
        recreate_collection: bool = False
):
    """
    Ingest markdown files into Milvus with hybrid search support.

    Args:
        md_dir: Directory containing markdown files
        batch_size: Number of documents to batch before inserting
        recreate_collection: If True, drop and recreate collection
    """

    # Initialize parser and vector store
    fm_parser = FinanceMarkdownParser()
    mv = MilvusVectorSave()

    # Create collection if needed
    log.info(f"Setting up collection: {COLLECTION_NAME}")
    mv.create_collection(recreate=recreate_collection)

    # Create connection
    mv.create_connection()

    # Process files
    batch: list[Document] = []
    total_doc_count = 0
    total_file_count = 0

    log.info(f"Starting ingestion from: {md_dir}")

    for root, _, files in os.walk(md_dir):
        md_files = sorted([f for f in files if f.endswith(".md")])

        for filename in md_files:
            filepath = os.path.join(root, filename)

            try:
                log.info(f"Processing: {filename}")

                # Parse markdown into chunks
                docs = fm_parser.parse_markdown_to_documents(filepath)

                if not docs:
                    log.warning(f"No chunks extracted from {filename}")
                    continue

                batch.extend(docs)
                total_file_count += 1

                # Insert batch when full
                if len(batch) >= batch_size:
                    log.info(f"Inserting batch of {len(batch)} chunks...")
                    mv.add_documents(batch)
                    total_doc_count += len(batch)
                    batch.clear()
                    log.info(f"Progress: {total_doc_count} chunks from {total_file_count} files")

            except Exception as e:
                log.error(f"Error processing {filename}: {e}")
                continue

    # Insert remaining documents
    if batch:
        log.info(f"Inserting final batch of {len(batch)} chunks...")
        mv.add_documents(batch)
        total_doc_count += len(batch)

    log.info("=" * 80)
    log.info(f"Ingestion complete!")
    log.info(f"Total files processed: {total_file_count}")
    log.info(f"Total chunks created: {total_doc_count}")
    log.info(f"Collection: {COLLECTION_NAME}")
    log.info("=" * 80)

    return total_doc_count, total_file_count


def verify_ingestion():
    """Verify that documents were successfully ingested."""
    from pymilvus import MilvusClient
    from config.paths import MILVUS_URI

    client = MilvusClient(uri=MILVUS_URI)

    if COLLECTION_NAME not in client.list_collections():
        log.error(f"Collection {COLLECTION_NAME} not found!")
        return False

    # Get collection stats
    stats = client.get_collection_stats(COLLECTION_NAME)
    row_count = stats.get("row_count", 0)

    log.info(f"Collection verification: {row_count} documents in {COLLECTION_NAME}")

    return row_count > 0


def test_search():
    """Test the hybrid search functionality."""
    from documents.milvus_db import get_hybrid_retriever

    log.info("Testing hybrid search...")

    retriever = get_hybrid_retriever(k=5, score_threshold=0.1)

    test_queries = [
        "What is a call option?",
        "Explain the Black-Scholes formula",
        "What is quantitative finance?"
    ]

    for query in test_queries:
        log.info(f"\nQuery: {query}")
        results = retriever.invoke(query)
        log.info(f"Found {len(results)} results")

        if results:
            top_result = results[0]
            log.info(f"Top result title: {top_result.metadata.get('title', 'N/A')}")
            log.info(f"Top result preview: {top_result.page_content[:150]}...")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest markdown files into Milvus")
    parser.add_argument(
        "--md-dir",
        type=str,
        default=MD_PATH,
        help="Directory containing markdown files"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Batch size for ingestion"
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Drop and recreate collection"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify ingestion after completion"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test searches after ingestion"
    )

    args = parser.parse_args()

    # Run ingestion
    total_docs, total_files = ingest_markdown_files(
        md_dir=args.md_dir,
        batch_size=args.batch_size,
        recreate_collection=args.recreate
    )

    # Verify if requested
    if args.verify:
        if verify_ingestion():
            log.info("✓ Verification passed")
        else:
            log.error("✗ Verification failed")

    # Test if requested
    if args.test:
        test_search()