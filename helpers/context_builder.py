def context(query: str, vectordb, k=5):
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)
    return docs


