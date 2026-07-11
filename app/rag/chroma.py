from pathlib import Path

import chromadb

BASE_DIR = Path(__file__).resolve().parents[2]

client = chromadb.PersistentClient(path=str(BASE_DIR / "vector_db"))

def get_collection():
    return client.get_or_create_collection("knowledge")
