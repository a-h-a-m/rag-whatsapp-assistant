from app.agents.registry import TOOLS

for tool in TOOLS:
    print(tool.name)
    print(tool.description)
    print("-" * 40)