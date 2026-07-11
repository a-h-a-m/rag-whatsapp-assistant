from fastapi import FastAPI

from app.routes import test, webhook

app = FastAPI()

app.include_router(webhook.router)
app.include_router(test.router)


@app.get("/")
def home():
    return {"message": "WhatsApp AI Bot running"}
