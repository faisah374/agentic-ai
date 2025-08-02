
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key  = gemini_api_key,
     base_url ="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )
capital_agent=Agent(
    name="capital_agent",
    instructions="You are a tool agent that tells the capital of the country.",
    handoff_description="tell me capital of any country"
)

language_agent=Agent(
    name="language_agent",
    instructions="You are a tool agent that tells the official language of the country.",
    handoff_description="your are language about any country"
)
population_agent=Agent(
    name="population_agent",
    instructions="You are a tool agent that tells the population of the country.",
    handoff_description="your tell about population tell any country"
)

orchestrator_agent=Agent(
        name="orchestrator_agent",
        instructions="You are an orchestrator agent that takes the country name and uses all 3 tools to give complete information about the country.",
        tools=[
            capital_agent.as_tool(
                tool_name="telling_capital",
                tool_description="A tool to tell the capital of the country."
            ),
            language_agent.as_tool(
                tool_name="telling_language",
                tool_description="A tool to tell the official language of the country."
            ),
            population_agent.as_tool(
                tool_name="telling_population",
                tool_description="A tool to tell the population of the country."

            )
        ],
        model=model,
)
async def main():
    msg=input("Enter the country name: ")
    result = await Runner.run(
        population_agent,
        input=msg,
        )

    print(result.final_output)
if __name__ == "__main__":
 asyncio.run(main())
