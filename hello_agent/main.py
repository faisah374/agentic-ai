import asyncio
from openai  import AsyncOpenAI
from agents  import Agent,OpenAIChatCompletionsModel,Runner,set_tracing_disabled

gemini_api_key ="AIzaSyAaA4GXzOkrtj4__Y2fRqtOPvERLeXSXT0"
client =AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

async def main():
    agent=Agent(
        name="Assistant",
        instructions="you  only respond in haiku",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=client),
    )
    result =await Runner.run(
        agent,
        "tell  me about recursion in programming,about pakistan"
    )
    print(result.final_output)
if __name__ == "__main__":
     asyncio.run(main())

