def build_tool_prompt(tools, question, formatted_history):

    tool_list = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])

    return f"""
You are an AI assistant.

Available tools:

{tool_list}

Your job is to decide which tool should answer the user's question.

Return ONLY valid JSON.

Example:

{{
    "tool": "calculator",
    "query": "25*48"
}}

If no tool is appropriate, return:

{{
    "tool": "none",
    "query": ""
}}

Conversation:

{formatted_history}

Current user question:

{question}
"""
