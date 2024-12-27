from langchain_chroma import Chroma


def initialize_vector_store(embedding_function):
    return Chroma(embedding_function=embedding_function)


def add_documents_to_store(vector_store, documents):
    return vector_store.add_documents(documents=documents)
