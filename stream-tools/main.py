import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,ItemHelpers,function_tool,WebSearchTool
from agents.run import RunConfig
from  dotenv import load_dotenv
import asyncio
import random
from openai.types import ResponseFormatText



load_dotenv()

gemini_api_key =os.getenv("GEMINI_API_KEY") 

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

@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)



async def main():
    agent = Agent(
        name="jokers",
        instructions="You are a helpful assistant. First, determine how many jokes to tell, then provide jokes.",
        tools=[how_many_jokes, WebSearchTool()],
    )

    result = Runner.run_streamed(agent, input="Hello,weather today in karachi")
    print(result)
    async for event in result.stream_events():
        if event.item.type == "tool_call_output_item":
            print(f"Tool output: {event.item.output}")
        elif event.item.type == "message_output_item":
            print(ItemHelpers.text_message_output(event.item))
if __name__ == "__main__":
 asyncio.run(main())
