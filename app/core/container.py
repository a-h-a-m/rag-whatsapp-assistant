from app.providers.gemini.chat import GeminiProvider
from app.memory.service import MemoryService
from app.agents.agent import Agent
from app.providers.whatsapp.green_api import GreenAPIProvider
from app.core.config import (
    GREEN_API_INSTANCE_ID,
    GREEN_API_TOKEN
)

ai_provider = GeminiProvider()
memory = MemoryService()
agent = Agent(ai_provider, memory)

whatsapp_provider = GreenAPIProvider(
    GREEN_API_INSTANCE_ID,
    GREEN_API_TOKEN
)