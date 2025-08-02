



from dotenv import load_dotenv
import os
from agents import Agent,Runner,AsyncOpenAI,RunConfig, OpenAIChatCompletionsModel
from agents.run import RunConfig


load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

# setup openrouter client
external_client=AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    
)
model= OpenAIChatCompletionsModel(
    model="microsoft/phi-4-reasoning-04-30:free",
    openai_client=external_client,
)
config=RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
agent=Agent(
    name="asssistant",
    instructions="You are a helpful assistant.",
)
result=Runner.run_sync(
    agent,
    input="write essay about pakistan islamic history",
   run_config=config
 
)
print(result)
