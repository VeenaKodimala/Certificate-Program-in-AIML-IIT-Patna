from pathlib import Path
import hashlib
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from log_processing import logText_splitter1
from lexical_store import insert_chunks

"""1. Create chroma persistent client - to save the embeddings on disk."""
chromaClient = chromadb.PersistentClient(f"{Path(__file__).resolve().parent}/log_DB_store")

"""2. Crete ambedding function."""
embeddingFunc = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-m3")

"""3. Create/owerite the collection, with a pre-defined embedding function - LogsRepo."""
collection = chromaClient.get_or_create_collection(name="LogsRepo",embedding_function=embeddingFunc,metadata={"hnsw:space":"cosine"})


def get_existing_version(file_id,verbose=True) -> int:
        #get the max version number from collection, for the file_id.
        existChunks = collection.get(where={"file_id":file_id},include=["metadatas"])
    
        versions = [metadata["version"] 
                    for metadata in existChunks["metadatas"]
                    if metadata["version"] is not None]
        maxPrevVersion = max(versions) if versions else None
        if verbose:
             print(f"maxPrevVersion: {maxPrevVersion}")
    
        nxtVersion = (maxPrevVersion if maxPrevVersion else 0) + 1
        if verbose:
             print(f"nxtVersion: {nxtVersion}")

        return nxtVersion

def process_each_file(file_path,chunk_size,chunk_overlap,verbose=True):
    path = Path(file_path)
    if verbose:
            print(f"path: {path}")

    if not path.is_file():
        raise FileNotFoundError(f"Log file not found: {path}")

    #Read and decode the file.
    log_text = path.read_text(encoding="utf-8",errors="replace")

    #Get the category of the file that is being processed.
    log_category = str(path.parent.name)
    if verbose:
        print(f"log_category: {log_category}")
        print(f"path.name: {path.name}")
        print(f"str(path.name): {str(path.name)}")
        print(f"str(path.resolve()):: {str(path.resolve())}")
        print(f"path.resolve():: {path.resolve()}")


    #Chunking
    chunks = logText_splitter1(text=log_text,fileName=str(path.name),chunkSize=chunk_size,chunkOverlap=chunk_overlap,verbose=False)

    if verbose:
         print(f"No.of chunks returned for {file_path}: {len(chunks)}")

    #Create a unique id for every log file path, so taht it can be used as a unique identifier, even if we have similar log file names in different paths.
    #The below create a hexa decimal code for the encoded(str->bytes) file path.
    file_id=hashlib.sha256(
        str(path.resolve()).encode("utf-8")
    ).hexdigest()
    if verbose:
        print(f"file_path: {file_path}")
    file_id = file_id[:16]
    if verbose:
        print(f"file_path with 16 chars: {file_id}")

    currentVersion = get_existing_version(file_id=file_id,verbose=True)
    if verbose:
             print(f"currentVersion {currentVersion}")

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
         print(f"len(ids)-> {len(ids)} ::: len(metadatas)-> {len(metadatas)} ::: len(documents)-> {len(documents)}")
                    
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
         print("--------Insert into collection, completed successfully-----")
         prevVersion = currentVersion - 1

         collection.delete(
              where={
                   "$and":[
                        {"file_id":file_id},
                    {"version":prevVersion}
                   ]
              }
         )

    sql_insert_result=insert_chunks(file_id=file_id,file_name=path.name,file_path=file_path,log_category=log_category,chunks=chunks,verbose=True)
    if verbose:
         print(f"sql_insert_result: {sql_insert_result}")
             
    return len(chunks)     


def process_All_files(
        root_dir:str = "resources",
        chunk_size:int = 1000,
        chunk_overlap:int = 150,
        verbose=True

) -> dict:
    if verbose:
         print(f"Path(__file__).resolve().parent:: {Path(__file__).resolve().parent}")
         print(f"root:: {Path(__file__).resolve().parent / root_dir}")
    root = Path(__file__).resolve().parent / root_dir
    if verbose:
         print(f"Root Directory: {root}")
         

    if not root.is_dir():
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
                 print(f"Indexed file in vector DB: {str(path.name)} present in {str(path.resolve())}. Chunks returned: {count}")
                  

        except Exception as e:
             print(f"Failed inserting chunks: {path} :: {e}")

        if verbose:
             print(f"Total chunks: {total_chunks}")

        
    if verbose:
         print(f"Total chunks: {total_chunks}, results:: {results}")
                  
    return results     

         


    

    










