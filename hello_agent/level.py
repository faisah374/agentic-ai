from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel
from agents.run import RunConfig

gemini_api_key="AIzaSyAaA4GXzOkrtj4__Y2fRqtOPvERLeXSXT0"

external_client=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client

)
config=RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
agent=Agent(
    name="Assiant",instructions="you are help assiant"
)
result= Runner.run_sync(agent,"how are you ,tell me about American parlimenthouse",run_config=config)
print(result.final_output)