from app.providers.gemini.provider import GeminiProvider
from app.rag.service import answer_question


provider = GeminiProvider()


answer = answer_question(
    # "Can employees work remotely?",
    "What is the CEO's favorite color?",
    provider
)


print(answer)