from app.providers.gemini.embeddings import GeminiEmbeddingProvider
from app.rag.retriever import retrieve_context

provider = GeminiEmbeddingProvider()

results = retrieve_context(
    "How many annual leave days?",
    provider
)

print(results)