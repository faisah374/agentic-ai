import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from agents.run import RunConfig 
from dotenv import load_dotenv

load_dotenv()

gemini_api_key= os.getenv("GEMINI_API_KEY")


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

# Agent specializing in billing inquiries
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle all billing-related inquiries. Provide clear and concise information regarding billing issues."
)

# Agent specializing in refund processes
refund_agent = Agent(
    name="Refund Agent",
    instructions="You handle all refund-related processes. Assist users in processing refunds efficiently."
)

# Triage agent that decides which specialist agent to hand off tasks to
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent should handle the user's request based on the nature of the inquiry.",
    handoffs=[billing_agent, refund_agent]
)

result=Runner.run_sync(triage_agent,input= "I need a billing for my recent purchase.",run_config=config)

print(result.final_output)