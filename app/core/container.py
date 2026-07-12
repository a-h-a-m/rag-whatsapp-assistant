from app.agents.agent import Agent
from app.core.config import GREEN_API_INSTANCE_ID, GREEN_API_TOKEN
from app.graph.checkpointer import checkpointer
from app.memory.service import MemoryService
from app.providers.gemini.chat import GeminiProvider
from app.providers.whatsapp.green_api import GreenAPIProvider
from app.rag.graph.workflow import create_graph
from app.rag.prompt import build_rag_prompt
from app.rag.retriever import retrieve_context

ai_provider = GeminiProvider()
memory = MemoryService()
rag_graph = create_graph(
    ai_provider,
    retriever=retrieve_context,
    prompt_builder=build_rag_prompt,
)
agent = Agent(
    ai_provider, 
    memory,
    rag_graph=rag_graph,
    checkpointer=checkpointer,
)

whatsapp_provider = GreenAPIProvider(GREEN_API_INSTANCE_ID, GREEN_API_TOKEN)
