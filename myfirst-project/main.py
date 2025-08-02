from dotenv import load_dotenv
import os
from agents import Agent,Runner,AsyncOpenAI, OpenAIChatCompletionsModel 
from agents.run import RunConfig
load_dotenv()
gemini_api_key= os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


agent=Agent(
    name="translator",
    instructions="You are a translator. Translate the text to the target language."
)
result= Runner.run_sync(
    agent,
    input="Translate 'Hello, how are you?, my name faisal hameed student in giaic' to urdu.",
     run_config=config
)
print(result)
