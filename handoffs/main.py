import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,RunConfig,handoffs
from dotenv import load_dotenv
load_dotenv()

gemini_api_key= os.getenv("GEMINI_API_KEY")


#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(api_key=gemini_api_key,

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
agent1:Agent=Agent(name="NextJS Agent",instructions="your are a helpful assistant")

agent2:Agent=Agent(name="Python Agent",instructions="your are a helpful assistant")

tri_Agent=Agent(
    name="tri agent",
    instructions="you talk is to delgate the request to the  approppiate a",
    handoffs=[agent1,agent2]
)

result=Runner.run_sync(tri_Agent,input="what is routing in NextJs?",run_config=config)

print(result.final_output)