from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GROQ_API_KEY")
client=Groq(api_key=api_key)

def generate_query(query:str, system_prompt:str):
    completion=client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "system",
        "content": system_prompt
      },
      {
        "role": "user",
        "content": query
      }
    ]
)
    return completion.choices[0].message.content

if __name__ == "__main__":
    print(generate_query("Hello, how are you?", "You are an assistant that helps users with their questions"))
