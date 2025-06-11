import os
import requests
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

CHROMA_PATH = os.getenv("CHROMA_DB_DIR", "./vector_store")
EMBED_MODEL = "all-MiniLM-L6-v2"

def get_vectorstore():
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectordb = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedder
    )
    return vectordb