from fastapi import APIRouter
from app.providers.whatsapp.green_api import GreenAPIProvider
from app.core.config import (
    GREEN_API_INSTANCE_ID,
    GREEN_API_TOKEN
)

router = APIRouter()


@router.get("/send-test")
def send_test():

    whatsapp = GreenAPIProvider(
        GREEN_API_INSTANCE_ID,
        GREEN_API_TOKEN
    )

    result = whatsapp.send_text(
        "6285877035941@c.us",
        "Hello from my Python AI bot!"
    )

    return {
        "result": result
    }