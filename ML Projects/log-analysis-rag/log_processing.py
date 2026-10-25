from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

from logger_config import get_logger

logger = get_logger(__name__)

def logText_splitter1(text:str,  fileName: str,chunkSize: int=1000, chunkOverlap:int =200,verbose=True):

    if not text.strip():
        logger.error("Log file is empty: %s", fileName)
        raise ValueError("Log file is empty.")
    if (chunkSize <= 0 or chunkOverlap <=0 or chunkOverlap >= chunkSize):
        logger.error("Invalid chunk settings for %s: chunkSize=%s, chunkOverlap=%s", fileName, chunkSize, chunkOverlap)
        raise ValueError("Chunk size and chunk overlap values are incorrect.")

    logger.debug("Splitting %s (chunkSize=%s, chunkOverlap=%s)", fileName, chunkSize, chunkOverlap)

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunkSize,chunk_overlap=chunkOverlap,add_start_index=True,strip_whitespace=False)

    documents = splitter.create_documents([text])
    chunks=[]

    for doc in documents:
        startIdx = doc.metadata["start_index"] + 1
        if verbose:
            logger.debug("len(doc.page_content): %s", len(doc.page_content))
        endIdx = startIdx + len(doc.page_content) - 1
        startLine = text.count("\n",0,startIdx)+1
        endLine = text.count("\n",0,endIdx)
        if verbose:
            logger.debug("text[endIdx-1]: %r", text[endIdx-1])
        if(text[endIdx-1] != "\n"):
            endLine += 1

        chunks.append(
            {
                "text":doc.page_content,
                "meta_data":{
                    "file_name":fileName,
                    "Start Index":startIdx,
                    "End Index":endIdx,
                    "Start Line":startLine,
                    "End Line":endLine
                }
            }
        )
    logger.info("Split %s into %d chunks", fileName, len(chunks))
    return chunks













 
    
