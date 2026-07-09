import chromadb

client = chromadb.PersistentClient(path="vector_db")

collection = client.get_collection("knowledge")

def retrieve_context(query, embedding_provider, limit=3):

    vector = embedding_provider.embed(query)

    results = collection.query(
        query_embeddings=[vector],
        n_results=limit
    )

    return results["documents"][0]