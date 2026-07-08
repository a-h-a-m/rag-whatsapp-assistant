from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    print("Received message:")
    print(data)

    return {
        "status": "received"
    }