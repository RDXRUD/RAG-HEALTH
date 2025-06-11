import os
import sys
from fastapi import FastAPI, Request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helpers.text_llm import query_llm

from helpers.prompt_builder import build_prompt

app = FastAPI()

@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    question = data.get("question")
    context = data.get("context")
    print("Received JSON:", data)
    if not question:
        return {"error": "No query provided"}
    prompt=build_prompt(question,context)
    response= query_llm(prompt)
    print(response.strip())
    return {"answer": response.strip(), "sources": [{
            **d["metadata"],      # unpack all metadata fields
            "content": d["page_content"]  # add content field
        } for d in context],"context":context}