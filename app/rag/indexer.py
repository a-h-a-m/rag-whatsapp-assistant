from pathlib import Path
import uuid
import chromadb

from app.providers.gemini.embeddings import GeminiEmbeddingProvider
from app.rag.chunker import chunk_text


def build_index():

    print("BUILD INDEX STARTED")

    client = chromadb.PersistentClient(
        path="vector_db"
    )

    collection = client.get_or_create_collection(
        "knowledge"
    )

    embedding = GeminiEmbeddingProvider()

    knowledge = Path("knowledge")

    print("Current folder:", Path.cwd())
    print("Knowledge exists:", knowledge.exists())
    print("Files:", list(knowledge.glob("*")))

    for file in knowledge.glob("*.txt"):

        text = file.read_text()

        chunks = chunk_text(text)

        for chunk in chunks:

            vector = embedding.embed(chunk)

            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[vector],
                metadatas=[
                    {
                        "source": file.name
                    }
                ]
            )


if __name__ == "__main__":
    build_index()