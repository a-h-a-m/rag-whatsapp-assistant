# tests/test_chroma.py

import chromadb


client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_collection(
    "knowledge"
)


print(
    "Documents:",
    collection.count()
)