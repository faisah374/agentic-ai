import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
def main():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of pakistan?"},
        ],
    )
    print(response['choices'][0]['message']['content'])
    
if __name__ == "__main__":
    main()
