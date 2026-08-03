### ---------------------------------------IMPORTS---------------------------------------------------
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
from pydantic import BaseModel
import chromadb
from IPython.display import Markdown,display
from fastapi import FastAPI
import uuid
from contextlib import asynccontextmanager
import threading

### ---------------------------API Key loading from .env file---------------------------------------

load_dotenv()
groqAPIKey = os.getenv("GroqAPIKey")

client = OpenAI(api_key=groqAPIKey,base_url="https://api.groq.com/openai/v1")

chromaClient = chromadb.Client()

###-----------------------------------Initializing the Logger----------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
logger=logging.getLogger(__name__)

###-----------------------------------Load and Index Data--------------------------------------------

def loadAndIndexDocs(verbose):
    docFolder = os.path.join(os.path.dirname("__file__"),"..","Documents")
    if verbose:
        print(f"Documents are in '{docFolder}' folder.")

    try:
        chromaClient.delete_collection("NovaTechData")
    except:
        pass

    collection=chromaClient.create_collection("NovaTechData")

    allChunks=[]
    allChunkIds=[]
    allMetadata=[]
    chunkID=1

    for fileName in os.listdir(docFolder):
        
        if not fileName.endswith("txt"):
            continue

        filePath = os.path.join(docFolder,fileName)
        if verbose:
            print(filePath)
        with open(filePath,"r") as cntxtMngr:
            text = cntxtMngr.read()
            if verbose:
                print(text[:10])

        text = text.replace("=",'')
        words = text.split()
        chunkSize=100
        overlap=20

        for i in range(0,len(words),chunkSize-overlap):
            chunk = ' '.join(words[i:i+chunkSize])
            allChunks.append(chunk)
            allChunkIds.append(f"Chunk_{chunkID}")
            allMetadata.append({"source":fileName})
            chunkID+=1

        if verbose:
            print(f"allChunkIds: \n{allChunkIds}")    
            print(f"allChunks: \n{allChunks}")


    collection.add(documents=allChunks,ids=allChunkIds,metadatas=allMetadata)
    logger.info(f"Indexed {chunkID} from {docFolder}")
    return collection



        #print(words)

###------------------------------------Defining the RAG function--------------------------------------

def askRAG(userQry,topK=3):
    #vectorCollc = loadAndIndexDocs(False)
    usrQryResult = vectorCollc.query(query_texts=[userQry],n_results=topK)
    usrQryChunks = usrQryResult["documents"][0]

    sources = [m["source"] for m in usrQryResult["metadatas"][0]]

    context = "\n\n".join(usrQryChunks)

    message = [{
        "role":"system",
        "content":"You are an useful assistent of NovaTech solutions. Answer the question only from the provided information. If the enough inormation to answer the user query is not available, then reply 'I do not have enough information to answer this question'."
    },
    {
        "role":"user",
        "content": f"Context: \n{context}\n\nmetadata: \n{sources}\n\nUser Question:\n{userQry}"
    }]

    llmResult = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=message
    )

    logger.info(f"Response received from LLM: {llmResult}")

    return llmResult.choices[0].message.content, list(sources)

   
###-----------------------------------Configuring FastAPI---------------------------------------------

def indexDocuments():
    global vectorCollc
    vectorCollc = loadAndIndexDocs(False)

@asynccontextmanager
async def lifespan(app:FastAPI):
    threading.Thread(target=indexDocuments,daemon=True).start()
    yield





api = FastAPI(title="NovaTech ChatBot",version="1.0",lifespan=lifespan)

#Configuring Request and Response classes for API

class ChatRequest(BaseModel):
    question:str

class ChatResponse(BaseModel):
    answer:str
    sources:list[str]
    requestID: str

@api.get("/")
def home():
    return {"stataus":"success","message":"NovaTech ChatBot is Up!!!"}

@api.post("/chat",response_model=ChatResponse)
def chat(request:ChatRequest):
    reqID = str(uuid.uuid4())[:8]
    logger.info(f"Request ID: {reqID}")

    answer,sources = askRAG(request.question)

    return ChatResponse(
        answer=answer,
        sources=sources,
        requestID=reqID
    )






