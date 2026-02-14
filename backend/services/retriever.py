from backend.services.embeddings import get_embedding
from backend.vectorstore.faiss_store import search

def retrieve(query):
    query_embedding = get_embedding(query)
    return search(query_embedding)
