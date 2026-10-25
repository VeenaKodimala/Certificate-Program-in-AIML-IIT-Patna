from log_processing import logText_splitter1
from vector_store import process_All_files
from logger_config import get_logger

logger = get_logger(__name__)

def test_log_splitter():
    sample_logs="""2026-10-20 10:00:01 INFO Service started
    2026-10-20 10:00:05 ERROR Database connection failed
    2026-10-20 10:00:06 INFO Retrying connection
    """

    logger.info("Running test_log_splitter")
    chunks = logText_splitter1(sample_logs,"serverlogs",50,10)
    logger.info("Chunks: %s", chunks)

def test_index_logFiles():
    logger.info("Running test_index_logFiles")
    results=process_All_files(root_dir="log_files",chunk_size=1000,chunk_overlap=150,verbose=True)
    logger.info("Results: %s", results)


if __name__ == "__main__":
    test_index_logFiles()    
