import requests

from app.core.config import GEMINI_API_KEY


class GeminiEmbeddingProvider:

    def embed(self, text):
        ...