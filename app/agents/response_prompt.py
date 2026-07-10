def build_response_prompt(question, tool_name, tool_result):

    return f"""
You are a helpful AI assistant.

The user asked:

{question}

The selected tool was:

{tool_name}

The tool returned:

{tool_result}

Answer the user's question naturally.

Do not mention internal tools.
"""