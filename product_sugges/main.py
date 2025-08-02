import os
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel
from  dotenv import load_dotenv
from agents.run import RunConfig
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

agent = Agent(
    name="Product Suggestion Agent",
    instructions="You are a product suggestion agent. You will suggest products based on user input.",
)
result=Runner.run_sync(agent,input="I have a headache, it should suggest pain relievers and medicine explain",run_config=config)
print(result.final_output)

  # Output the result of the agent's suggestion