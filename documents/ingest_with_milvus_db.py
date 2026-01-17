# Using a Distributed, Multi-Process Approach to Write Massive Data into the Milvus Database
import multiprocessing
import os
from multiprocessing import Queue

from config.paths import MD_PATH
from documents.md_parser import FinanceMarkdownParser
from documents.milvus_db import MilvusVectorSave
from utils.log_utils import log


def file_parser_process(dir_path: str, output_queue: Queue, batch_size: int = 20):
    #using batching can decrease the usage of RAM
    """
    Process 1: parse all markdown files under the directory and put them into queue in batches
    :param dir_path:
    :param output_queue:
    :param batch_size:
    :return:
    """
    log.info(f"Parsing process starts and scan the directory: {dir_path}.")

    #get all .md file
    md_files = [
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if f.endswith(".md")
    ]

    if not md_files:
        log.warning("Warning: no markdown files found.")
        output_queue.put(None) #.put() is a function to insert content to Queue instance
        return

    parser = FinanceMarkdownParser()
    doc_batch = []
    for file_path in md_files:
        try:
            docs = parser.parse_markdown_to_documents(file_path)
            if docs:
                doc_batch.extend(docs)
            #put it to queue in batches
            if len(doc_batch) >= batch_size:
                output_queue.put(doc_batch.copy()) #insert a copy to the queue
                doc_batch.clear() #clear all the batches in current buffer
        except Exception as e:
            log.warning(f"Error while parsing {file_path}: {str(e)}")
            log.exception(e)

    #insert leftover docs
    if doc_batch:
        output_queue.put(doc_batch)
        #no need to use .copy() and .clear() because we won't use doc_batch anymore

    #finishing
    output_queue.put(None)
    log.info(f"Parsing process ends and processed {len(md_files)} documents.")


def milvus_writer_process(input_queue: Queue):
    """
    Process 2: read the queue and write the result to Milvus
    :param input_queue:
    :return:
    """
    mv = MilvusVectorSave()
    mv.create_connection()

    total_count = 0
    while True:
        try:
            #A blocking function is a function that prevents further execution of the program until it completes its task.
            #When a blocking function is called, the program must wait for it to finish before proceeding to the next instruction.
            datas = input_queue.get() # blocking function
            if datas is None: #receives signal of ending
                break
            if isinstance(datas, list):
                mv.add_documents(datas)
                total_count += len(datas)
                log.info(f"Added {len(datas)} documents.")
        except Exception as e:
            log.warning(f"Error while writing.")
            log.exception(e)

    log.info(f"Milvus writer process ends and processed {total_count} documents.")


if __name__ == '__main__':
    # configure parameters
    md_dir = str(MD_PATH)  # Markdown file directory
    queue_maxsize = 20  # max capacity of the queue to prevent RAM overload

    mv = MilvusVectorSave()
    mv.create_collection()
    mv.create_connection()

    # create queue
    docs_queue = Queue(maxsize=queue_maxsize)

    # initiate child processes
    parser_proc = multiprocessing.Process(
        target=file_parser_process,
        args=(md_dir, docs_queue)
    )
    writer_proc = multiprocessing.Process(
        target=milvus_writer_process,
        args=(docs_queue,)
    )

    parser_proc.start()
    writer_proc.start()

    # wait for the processes to end
    parser_proc.join()
    writer_proc.join()

    print("System notification: all tasks are done.")