
from dotenv import load_dotenv
from agents import Agent,Runner,AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
import os
import asyncio
from agents.run import RunConfig
import functools
load_dotenv()
async def main():
    Model_Name = "gemini-1.5-flash"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    external_client=AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    model=OpenAIChatCompletionsModel(
        model=Model_Name,
        openai_client=external_client,
    ) 

    config= RunConfig(
    model=model,
    model_provider= external_client,
    tracing_disabled=True,
  
    )
    @function_tool(name_override='feacth_weather'
                  description_override='location to fecth karo'
    )
    def weather_fetcher(location:str) -> str:
        print (f"The weather in {location} is sunny.")
    return  f"cloudly weather" 
    

    
    teacher =Agent(
        name="math teacher",
        instructions="you are a math teacher",
        model=model
        functools=weather_fetcher
    )
    prompt=input(enter your prompt)
    result= await Runner.run(teacher,"tell me answer to 10+10",prompt,run_config=config)
    print(result.final_output)

if __name__ == "__main__":
 asyncio.run(main())




    
    
    







