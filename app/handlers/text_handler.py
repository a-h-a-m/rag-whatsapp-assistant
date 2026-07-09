from app.rag.service import answer_question
from app.services.memory import (
    save_message,
    get_history
)



def handle_text_message(
    message,
    ai_provider,
    whatsapp_provider
):

    user_id = message["sender"]


    save_message(
        user_id,
        "user",
        message["text"]
    )


    history = get_history(
        user_id
    )


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


    answer = answer_question(
        message["text"],
        ai_provider,
        history
    )


    save_message(
        user_id,
        "assistant",
        answer
    )



    whatsapp_provider.send_text(
        user_id,
        answer
    )