from fastapi import APIRouter, Request

from app.core.container import (
    ai_provider,
    whatsapp_provider
)

from app.services.message_parser import extract_message
from app.handlers.audio_handler import handle_audio_message
from app.handlers.text_handler import handle_text_message


router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    # print(data)

    message = extract_message(data)

    print(message)


    if message["type"] == "audioMessage":

        handle_audio_message(message, ai_provider, whatsapp_provider)

    elif message["type"] == "textMessage":

        handle_text_message(message, ai_provider, whatsapp_provider)

    return {
        "status": "ok"
    }