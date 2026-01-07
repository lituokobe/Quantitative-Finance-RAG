import os
import multiprocessing
from multiprocessing import Queue
from typing import Callable
from langchain_core.documents import Document
from config.paths import MD_PATH, QWEN3_EMBEDDING_PATH
from documents.md_parser import FinanceMarkdownParser
from documents.milvus_chunk_writer import MilvusChunkWriter
from models.models import Qwen3CustomEmbedding
from utils.log_utils import log

# --------------------------------------------------
# Parser process
# --------------------------------------------------
def parser_process(md_dir: str, output_queue: Queue, batch_size: int = 32):
    parser = FinanceMarkdownParser()
    batch: list[Document] = []

    for root, _, files in os.walk(md_dir):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue

            path = os.path.join(root, f)
            try:
                docs = parser.parse_markdown_to_documents(path)
                batch.extend(docs)

                if len(batch) >= batch_size:
                    if output_queue.full():
                        log.info("[Parser] Queue full, waiting...")
                    output_queue.put(batch.copy())
                    batch.clear()
                    log.info(f"[Parser] Pushed batch of {batch_size} chunks.")

            except Exception as e:
                log.error(f"[Parser] Error parsing {path}: {e}")

    if batch:
        output_queue.put(batch)
        log.info(f"[Parser] Pushed final batch of {len(batch)} chunks.")

    output_queue.put(None)
    log.info("[Parser] Done.")

# --------------------------------------------------
# Writer process
# --------------------------------------------------
def writer_process(
    input_queue: Queue,
    collection_name: str,
    embedding_factory: Callable[[], Qwen3CustomEmbedding],
    dim: int,
    host: str = "localhost",
    port: str = "19530",
    metric_type: str = "IP",
):
    # Instantiate embedding model INSIDE the process
    embedding_model = embedding_factory()
    writer = MilvusChunkWriter(
        collection_name=collection_name,
        embedding_fn=embedding_model.embed_documents,
        dim=dim,
        host=host,
        port=port,
        metric_type=metric_type,
    )

    writer.create_collection(recreate=False)
    total = 0

    while True:
        batch = input_queue.get()
        if batch is None:
            break

        try:
            n = writer.add_documents(batch)
            total += n
            log.info(f"[Writer] Inserted {n} chunks. Total={total}")
        except Exception as e:
            log.error(f"[Writer] Error inserting batch: {e}")

    writer.flush()
    log.info(f"[Writer] Done. Inserted {total} chunks.")

# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == "__main__":
    QUEUE_SIZE = 4
    COLLECTION_NAME = "finance_chunks"
    DIM = 2560  # example: Qwen3 embedding dimension

    def create_embedding_model() -> Qwen3CustomEmbedding:
        return Qwen3CustomEmbedding(str(QWEN3_EMBEDDING_PATH))

    docs_queue = Queue(maxsize=QUEUE_SIZE)

    p1 = multiprocessing.Process(
        target=parser_process,
        args=(MD_PATH, docs_queue, 6),
    )
    p2 = multiprocessing.Process(
        target=writer_process,
        args=(docs_queue, COLLECTION_NAME, create_embedding_model, DIM),
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    log.info("Ingestion finished.")