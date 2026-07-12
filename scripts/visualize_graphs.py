
from app.agents.executor import ToolExecutor
from app.agents.registry import get_tools
from app.agents.responder import ResponseGenerator
from app.agents.selector import ToolSelector
from app.core.container import (
    ai_provider,
    memory,
)
from app.graph.workflow import create_graph
from app.rag.graph.workflow import create_graph as create_rag_graph
from app.rag.prompt import build_rag_prompt
from app.rag.retriever import retrieve_context

rag_graph = create_rag_graph(
    provider=ai_provider,
    retriever=retrieve_context,
    prompt_builder=build_rag_prompt,
)

tools = get_tools()

agent_graph = create_graph(
    tools=tools,
    selector=ToolSelector(ai_provider, tools),
    executor=ToolExecutor(tools),
    responder=ResponseGenerator(ai_provider),
    memory=memory,
)

# agent = agent_graph.get_graph().draw_mermaid()
# rag = rag_graph.get_graph().draw_mermaid()

# docs = Path("docs/graphs")
# docs.mkdir(parents=True, exist_ok=True)

# (docs / "agent.md").write_text(
#     f"""# Agent Graph

# ```mermaid
# {agent}
# ```""",
# encoding="utf-8",
# )

# (docs / "rag.md").write_text(
#     f"""# RAG Graph

# ```mermaid
# {rag}
# ```""",
# encoding="utf-8",
# )

print("=== Agent ===")
print(agent_graph.get_graph().draw_mermaid())

print()
print("=== RAG ===")
print(rag_graph.get_graph().draw_mermaid())