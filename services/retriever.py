import os
import sys
from fastapi import FastAPI, Request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.context_builder import context
from helpers.db_init import get_vectorstore

app = FastAPI()
vectordb = get_vectorstore()

@app.post("/retrieve")
async def retrieve(req: Request):
    ques = await req.json()
    question = ques.get("query")
    print("Received JSON:", ques)
    if not question:
        return {"error": "No query provided"}

    docs = context(question, vectordb)
    print(docs)
    return {"question":question,"context": docs}