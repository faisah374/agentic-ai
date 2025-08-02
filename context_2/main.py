import os
from dotenv import load_dotenv
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,set_tracing_disabled
import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool
load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key=os.getenv("GEMINI_API_KEY")

external_client=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)
# Define a simple context using a data class
@dataclass
class UserInfo:  
    name: str
    uid: int
    location:str="pakistan"

# A tool function that accesses local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 44 years old"
@function_tool
async def fetch_loaction(wrapper:RunContextWrapper[UserInfo]) ->str :
  return f"user {wrapper.context.name} is {wrapper.context.location} " 

async def main():
    # Create your context object
    user_info = UserInfo(name="Qasim", uid=123)  

    # Define an agent that will use the tool above
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age,fetch_loaction],
        model=model,
    )

    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of user?  currrent loacation of  user?",
        context=user_info,
    )

    print(result.final_output)  # Expected output: The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())