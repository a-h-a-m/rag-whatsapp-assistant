from fastapi import APIRouter, HTTPException, Request

from app.core.container import agent, ai_provider, whatsapp_provider
from app.handlers.audio_handler import handle_audio_message
from app.handlers.text_handler import handle_text_message
from app.services.message_parser import extract_message

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    try:
        message = extract_message(data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    print(message)

    text = ""

    if message["type"] == "audioMessage":
        text = handle_audio_message(message, ai_provider, whatsapp_provider) # transcribe the audio first

    elif message["type"] == "textMessage" or message["type"] == "extendedTextMessage":
        text = message["text"]

    if text != "":
        message["text"] = text
        handle_text_message(message, agent, whatsapp_provider)

    else:
        return {"status": "ignored"}

    return {"status": "ok"}
