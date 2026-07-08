from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "WhatsApp AI Bot running"
    }