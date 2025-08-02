import os
from dotenv import load_dotenv

from  pydantic import BaseModel
from agents import Agent,RunContextWrapper,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,function_tool,enable_verbose_stdout_logging,Runner
from agents.run import RunConfig
from dataclasses import dataclass
from agents import set_tracing_disabled

import asyncio
set_tracing_disabled(disabled=True)
load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client

)
# config=RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True


# )

enable_verbose_stdout_logging()


@dataclass
class Userinfo:
  name:str
  uid:int
   
@function_tool
def userinfo(wrapper:RunContextWrapper[Userinfo])->str:
    """Return as greet message"""
    return f"Hello {wrapper.context.name}, you are 44 years old."
print (f"hello {Wrapper.context.uid}")
async def main():
  user_info=Userinfo(name="faisal",uid=4230)

  agent=Agent[Userinfo](
    name="Assitant",
    tools=[userinfo],
    model=model,
)
  result=await Runner.run(
     agent,
     input='what are name and age?',
     context=user_info,)
  
  print(result.final_output)

if __name__ == "__main__":
   asyncio.run(main())