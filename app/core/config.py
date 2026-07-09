import os
from dotenv import load_dotenv

load_dotenv()


GREEN_API_INSTANCE_ID = os.getenv(
    "GREEN_API_INSTANCE_ID"
)

GREEN_API_TOKEN = os.getenv(
    "GREEN_API_TOKEN"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)