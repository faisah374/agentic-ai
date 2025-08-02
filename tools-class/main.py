import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,ItemHelpers,function_tool,WebSearchTool
from agents.run import RunConfig
from  dotenv import load_dotenv
import asyncio
import random
from openai.types import ResponseFormatText
import requests


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
def get_weather(location: str) -> str:
    """
    Get the current weather for a given location.
    """
    result = requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={location}")

    if result.status_code == 200:
        data = result.json()
        return f"The weather in {location} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data."
    # Simulate a weather API call
    weather_data = {
        "karachi": "Sunny, 34°C",
        "Los Angeles": "Cloudy, 22°C",
        "Chicago": "Rainy, 18°C"
    }
    return weather_data.get(location, "Weather data not available for this location.")
agent=Agent(
    name="get weather",
    instructions="you are help assistant",
    tools=[get_weather],
    )
def run(message:str)->str:
    print("Run message",message)
    result=Runner.run_sync(agent, 
    f"{message}?", run_config=config,
    )
    return result.final_output

if __name__ == "__main__":
    print(run("what is the weather in karachi?"))