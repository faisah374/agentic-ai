import os
import asyncio
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig,set_tracing_disabled
from agents.run import Runner
from agents.run import Agent
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
set_tracing_disabled(disabled=True)

    # Load the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )




async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
        model=model,
    )
    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
         print(event.data.delta, end="", flush=True)

if __name__  == "__main__":
 asyncio.run(main())



   



    



