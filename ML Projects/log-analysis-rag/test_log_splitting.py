from log_processing import logText_splitter1
from vector_store import process_All_files

def test_log_splitter():
    sample_logs="""2026-10-20 10:00:01 INFO Service started
    2026-10-20 10:00:05 ERROR Database connection failed
    2026-10-20 10:00:06 INFO Retrying connection
    """

    chunks = logText_splitter1(sample_logs,"serverlogs",50,10)
    print(chunks)

def test_index_logFiles():
    results=process_All_files(root_dir="log_files",chunk_size=1000,chunk_overlap=150,verbose=True)
    print(results)


if __name__ == "__main__":
    test_index_logFiles()    
