
import os
from dotenv import load_dotenv
from typing import cast ,List
import chainlit as cl
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool
from agents.run_context import RunContextWrapper

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

    @cl.on_chat_starter
    async def starter() -> list[cl.starter]:
        return[
            cl.starter(
                label="Greeting",
                message="Hello! I am a GEMINI agent. How can I assist you today?",
                icon="🤖"
            ),
            cl.starter(
                label="weather",
                message="Find a weather in Karachi"
            ),
            
        ]
class MyContext:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.seen_messages =[]
        

        @function_tool
        @cl.step(type="weather_tool")
        def get_weather_info(location: str, unit: str = "c") -> str:
            """
            fetch weather  for a given location ,returning a  short description. 
            """
            return f"The weather in {location} is 22 degrees {unit}."

        @function_tool
        @cl.step(type="greeting_tool")
        def get_greeter_user(context:RunContextWrapper[MyContext],greeting: str)->str:
            user_id = context.user_id 
            return f"Hello {user_id},you said: {greeting}"
        
        @cl.on_chat_start
        async def on_chat_start():
            external_client = AsyncOpenAI(
                api_key=gemini_api_key,
                base_url="https://generativelanguage>googleapis.com/v1beta/openai/",
            )
            model = OpenAIChatCompletionsModel(
                openai_client=external_client,
                model_name="gemini/gemini-2.0-flash",
            )
            congfig = RunConfig(
                model=model,
                model_provider=external_client,
                tracing_enabled=True,
            )
            cl.user_session.set("config", congfig)
            agent:Agent=Agent(
                name="Assistant",
                tools=[get_greeter_user,get_weather_info],
                instructions="you are help assistant,call greet_user tool to greet user,Always greet the user when session starts.",
                model=model,
            )
            cl.user_session.set("agent", agent)

            await cl.Message(
                content="welcome to the panaversity AI Assistant! How can I assist you today?",
                
            ).send()
        @cl.on_message
        async def main(message:cl.Message):
            """process incoming messages and run the agent."""
            msg= cl.Message(content="Thinking...")
            await msg.send()

            agent: Agent= cast(Agent, cl.user_session.get("agent"))
            config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

            history = cl.user_session.get("history", [])

            history.append({"role": "user", "content": message.content})

            my_ctx= MyContext(user_id="Zia")
            result= Runner.run_sync(
                agent,
                history,
                run_config=config,
                my_context=my_ctx
            )
            print("\n[run_sync_result]\n",result,"\n")
            # try:
            #     print("\n[calling_Agent_with_context]\n",history,"\n")
            #     result=Runner.run_sync(agent,history,run_config=config,my_context=my_ctx)

            #     response_content=  result.final_output
            #     msg.content = response_content
            #     await msg.update()
            #     history.append({"role": "assistant", "content": response_content})
            #     cl.user_session.set("history", history)

            #     print(f"user:{message.content}") 
            #     print(f"assistant:{response_content}")
            # except Exception as e:
            #  msg.content = f"An error occurred: {str(e)}"
            # await msg.update()
            # print(f"Error: {e}")