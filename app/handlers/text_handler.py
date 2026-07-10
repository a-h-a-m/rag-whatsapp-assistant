# from app.rag.service import answer_question
# from app.services.memory import (
#     save_message,
#     get_history
# )



def handle_text_message(
    message,
    agent,
    whatsapp_provider
):

    text = message["text"]

    print("=" * 50)
    print("Incoming:", text)

    user_id = message["sender"]


    agent.memory.add_message(
        user_id,
        "user",
        text
    )


    # history = get_history(
    #     user_id
    # )


    # ai_messages = []


    # for item in history:

    #     ai_messages.append(
    #         {
    #             "role": item["role"],
    #             "parts": [
    #                 {
    #                     "text": item["content"]
    #                 }
    #             ]
    #         }
    #     )


    # answer = answer_question(
    #     message["text"],
    #     agent,
    #     history
    # )
    answer = agent.run(user_id, text)

    print("Selected Tool:", answer.tool)
    print(answer.query)
    print("Tool Result:", answer.tool_result)
    print("Final Response:", answer.response)

    print("=" * 50)

    agent.memory.add_message(
        user_id,
        "assistant",
        answer.response
    )



    whatsapp_provider.send_text(
        user_id,
        answer.response
    )