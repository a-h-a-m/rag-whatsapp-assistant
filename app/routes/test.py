from fastapi import APIRouter

from app.core.container import whatsapp_provider

router = APIRouter()


@router.get("/send-test")
def send_test():

    result = whatsapp_provider.send_text("6285877035941@c.us", "Hello from my Python AI bot!")

    return {"result": result}
