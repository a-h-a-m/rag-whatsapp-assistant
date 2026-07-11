from app.rag.chroma import get_collection


def retrieve_context(query, embedding_provider, limit=3):
    collection = get_collection()

    vector = embedding_provider.embed(query)

    results = collection.query(query_embeddings=[vector], n_results=limit)

    return results["documents"][0]
