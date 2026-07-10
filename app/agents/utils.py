from app.agents.registry import TOOLS


def get_tool(name: str):
    for tool in TOOLS:
        if tool.name == name:
            return tool

    return None