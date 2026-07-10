from app.providers.gemini.chat import GeminiProvider
from app.agents.agent import Agent


agent = Agent(
    GeminiProvider()
)

# print(agent.run("What time is it?"))

# print(agent.run("25 * 48"))

print(
    agent.run(
        "How many annual leave days?"
    )
)