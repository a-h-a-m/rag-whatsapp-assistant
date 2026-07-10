import requests
import base64

from app.core.config import GEMINI_API_KEY
from app.providers.ai_provider import AIProvider


class GeminiProvider(AIProvider):

    def chat(self, messages):
        
        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.1-flash-lite:generateContent"
        )


        payload = {
            "contents": messages
        }


        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            },
            json=payload
        )


        if not response.ok:
            print("Gemini error:")
            print(response.status_code)
            print(response.text)
            return None


        result = response.json()


        return (
            result["candidates"][0]
            ["content"]
            ["parts"][0]
            ["text"]
        )



    def transcribe(self, file_path):
        
        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-2.5-flash:generateContent"
        )


        with open(file_path, "rb") as audio_file:

            audio_base64 = base64.b64encode(
                audio_file.read()
            ).decode("utf-8")


        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Transcribe this audio"
                        },
                        {
                            "inline_data": {
                                "mime_type": "audio/ogg",
                                "data": audio_base64
                            }
                        }
                    ]
                }
            ]
        }


        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            },
            json=payload
        )


        if not response.ok:
            print("Gemini error:")
            print(response.status_code)
            print(response.text)
            return None


        result = response.json()


        return (
            result["candidates"][0]
            ["content"]
            ["parts"][0]
            ["text"]
        )



    def embed(self, text):
        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-embedding-2:embedContent"
        )

        payload = {
            "model": "models/gemini-embedding-2",
            "content": {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        }

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            },
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return data["embedding"]["values"]