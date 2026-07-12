def get_tool(tools, name: str):
    for tool in tools:
        if tool.name == name:
            return tool

    return None
