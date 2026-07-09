from app.providers.gemini.provider import GeminiProvider
from app.providers.whatsapp.green_api import GreenAPIProvider
from app.core.config import (
    GREEN_API_INSTANCE_ID,
    GREEN_API_TOKEN
)

ai_provider = GeminiProvider()

whatsapp_provider = GreenAPIProvider(
    GREEN_API_INSTANCE_ID,
    GREEN_API_TOKEN
)