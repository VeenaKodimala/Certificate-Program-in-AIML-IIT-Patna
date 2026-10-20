from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def logText_splitter1(text:str,  fileName: str,chunkSize: int=1000, chunkOverlap:int =200):

    if not text.strip():
        raise ValueError("Log file is empty.")
    if (chunkSize <= 0 or chunkOverlap <=0 or chunkOverlap >= chunkSize):
        raise ValueError("Chunk size and chunk overlap values are incorrect.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunkSize,chunk_overlap=chunkOverlap,add_start_index=True,strip_whitespace=False)

    documents = splitter.create_documents([text])
    chunks=[]

    for doc in documents:
        startIdx = doc.metadata["start_index"] + 1
        print("len(doc.page_content): ",len(doc.page_content))
        endIdx = startIdx + len(doc.page_content) - 1
        startLine = text.count("\n",0,startIdx)+1
        endLine = text.count("\n",0,endIdx)
        print("text[endIdx-1]: ",text[endIdx-1])
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
    return chunks













 
    
