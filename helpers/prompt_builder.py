from langchain_core.documents import Document

def build_prompt(query: str, docs: list[Document]) -> str:
    context = "\n\n".join(doc["page_content"] for doc in docs)
    # print(docs)
    return f"""[Context]\n{context}\n\n[Question]\n{query}\n\n[Answer]"""


