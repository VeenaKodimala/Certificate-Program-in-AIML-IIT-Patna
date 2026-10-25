import logging
from pathlib import Path
import hashlib
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from log_processing import logText_splitter1
from lexical_store import insert_chunks
from logger_config import get_logger

logger = get_logger(__name__)

#Setting the logger levels of the imported libs as warning.
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)

"""1. Create chroma persistent client - to save the embeddings on disk."""
chromaClient = chromadb.PersistentClient(f"{Path(__file__).resolve().parent}/log_DB_store")
logger.info("Chroma persistent client initialised")

"""2. Crete ambedding function."""
embeddingFunc = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-m3")
logger.info("Embedding function loaded: BAAI/bge-m3")

"""3. Create/owerite the collection, with a pre-defined embedding function - LogsRepo."""
collection = chromaClient.get_or_create_collection(name="LogsRepo",embedding_function=embeddingFunc,metadata={"hnsw:space":"cosine"})
logger.info("Collection ready: LogsRepo")


def get_existing_version(file_id,verbose=True) -> int:
        #get the max version number from collection, for the file_id.
        existChunks = collection.get(where={"file_id":file_id},include=["metadatas"])
    
        versions = [metadata["version"] 
                    for metadata in existChunks["metadatas"]
                    if metadata["version"] is not None]
        maxPrevVersion = max(versions) if versions else None
        if verbose:
             logger.debug("maxPrevVersion: %s", maxPrevVersion)
    
        nxtVersion = (maxPrevVersion if maxPrevVersion else 0) + 1
        if verbose:
             logger.debug("nxtVersion: %s", nxtVersion)

        return nxtVersion

def process_each_file(file_path,chunk_size,chunk_overlap,verbose=True):
    path = Path(file_path)
    if verbose:
            logger.debug("path: %s", path)

    if not path.is_file():
        logger.error("Log file not found: %s", path)
        raise FileNotFoundError(f"Log file not found: {path}")

    #Read and decode the file.
    log_text = path.read_text(encoding="utf-8",errors="replace")

    #Get the category of the file that is being processed.
    log_category = str(path.parent.name)
    if verbose:
        logger.debug("log_category: %s", log_category)
        logger.debug("path.name: %s", path.name)
        logger.debug("path.resolve(): %s", path.resolve())


    #Chunking
    chunks = logText_splitter1(text=log_text,fileName=str(path.name),chunkSize=chunk_size,chunkOverlap=chunk_overlap,verbose=False)

    if verbose:
         logger.debug("No.of chunks returned for %s: %d", file_path, len(chunks))

    #Create a unique id for every log file path, so taht it can be used as a unique identifier, even if we have similar log file names in different paths.
    #The below create a hexa decimal code for the encoded(str->bytes) file path.
    file_id=hashlib.sha256(
        str(path.resolve()).encode("utf-8")
    ).hexdigest()
    if verbose:
        logger.debug("file_id (16 chars) for %s: %s", file_path, file_id[:16])
    file_id = file_id[:16]

    currentVersion = get_existing_version(file_id=file_id,verbose=True)
    if verbose:
             logger.debug("currentVersion %s", currentVersion)

    ids=[]
    metadatas=[]
    documents=[]

    for id,chunk in enumerate(chunks):
         ids.append(f"{file_id}_{id}")
         documents.append(chunk["text"])

         metadata = chunk["meta_data"].copy()
         metadata["file_id"]=file_id
         metadata["file_name"]=path.name
         metadata["file_path"]=str(path.resolve())
         metadata["log_category"]=log_category
         metadata["version"]=currentVersion

         metadatas.append(metadata)

         #Store the chunk in chroma collection.
    if verbose:
         logger.debug("len(ids)=%d, len(metadatas)=%d, len(documents)=%d", len(ids), len(metadatas), len(documents))
                    
    if ids:
         collection.upsert(
              ids=ids,
              documents=documents,
              metadatas=metadatas
         )

    checkChunks = collection.get(
         where={
              "$and":[
                   {"file_id":file_id},
                    {"version":currentVersion}
              ]
         },
         include=["metadatas"]
    )     

    if len(checkChunks["ids"]) == len(ids):
         logger.info("Insert into collection completed successfully for %s (version %s)", path.name, currentVersion)
         prevVersion = currentVersion - 1

         collection.delete(
              where={
                   "$and":[
                        {"file_id":file_id},
                    {"version":prevVersion}
                   ]
              }
         )
    else:
         logger.warning("Chunk count mismatch for %s: expected %d, found %d. Previous version retained.", path.name, len(ids), len(checkChunks["ids"]))

    sql_insert_result=insert_chunks(file_id=file_id,file_name=path.name,file_path=file_path,log_category=log_category,chunks=chunks,verbose=True)
    if verbose:
         logger.debug("sql_insert_result: %s", sql_insert_result)
             
    return len(chunks)     


def process_All_files(
        root_dir:str = "resources",
        chunk_size:int = 1000,
        chunk_overlap:int = 150,
        verbose=True

) -> dict:
    if verbose:
         logger.debug("Path(__file__).resolve().parent: %s", Path(__file__).resolve().parent)
         logger.debug("root: %s", Path(__file__).resolve().parent / root_dir)
    root = Path(__file__).resolve().parent /"resources"/ root_dir
    if verbose:
         logger.info("Root Directory: %s", root)
         

    if not root.is_dir():
        logger.error("Logs directory not found: %s", root)
        raise NotADirectoryError(f"Logs directory not found: {root}")

    total_chunks=0
    results={}

    #Recursivel find every file under the root folder
    """Using rglob to recursively fetch all the files presnt in directory and sub directories.glob stops its retrieval till the root. It will not access sub directories."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        try:
            count = process_each_file(file_path=str(path),chunk_size=chunk_size,chunk_overlap=chunk_overlap)
            total_chunks = total_chunks + count
            results[str(path)]=count
            if verbose:
                 logger.info("Indexed file in vector DB: %s present in %s. Chunks returned: %d", path.name, path.resolve(), count)
                  

        except Exception as e:
             logger.exception("Failed inserting chunks: %s :: %s", path, e)

        if verbose:
             logger.debug("Total chunks: %d", total_chunks)

        
    if verbose:
         logger.info("Total chunks: %d, len(results): %d", total_chunks, len(results))
                  
    return results     

         


    

    










