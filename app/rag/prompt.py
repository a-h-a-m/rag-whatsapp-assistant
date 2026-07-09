def build_rag_prompt(contexts, question, history=None):

    context = "\n\n".join(contexts)

    if history:
        conversation = "\n".join(
            [
                f"{role}: {content}"
                for role, content in history
            ]
        )
    else:
        conversation = "No previous conversation."


    return f"""
You are a helpful assistant.

Use the conversation history to understand the user's intent.

Use the context below to answer questions about company information.

If the answer is not available in the context,
say:
"I don't have that information."

Conversation history:
{conversation}


Context:
{context}


Current question:
{question}

Answer:
"""