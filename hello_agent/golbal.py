from agents import Agent,Runner,AsyncOpenAI,set_default_openai_client,set_tracing_disabled,set_default_openai_api


gemini_api_key="AIzaSyAaA4GXzOkrtj4__Y2fRqtOPvERLeXSXT0"
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

extrnal_client=AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
set_default_openai_client(extrnal_client)

agent=Agent(
    name="Assistant",instructions="you are help assisant",model="gemini-2.0-flash"
)
result= Runner.run_sync(agent,"tell me about american congress  how can elected")

print(result.final_output)