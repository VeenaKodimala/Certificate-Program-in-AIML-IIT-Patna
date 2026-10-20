from pathlib import Path
import hashlib
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from log_processing import logText_splitter1

"""1. Create chroma persistent client - to save the embeddings on disk."""
chromaClient = chromadb.PersistentClient("./log_files")

"""2. Crete ambedding function."""
embeddingFunc = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-m3")

collection = chromaClient.get_or_create_collection(name="LogsRepo",embedding_function=embeddingFunc)






