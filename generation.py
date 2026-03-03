from groq import Groq
import os

# Load locally from .env if available (for development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try Streamlit secrets first (for Streamlit Cloud), then fall back to env var
try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_query(query:str, system_prompt:str):
    completion=client.chat.completions.create(
    model="openai/gpt-oss-120b",
    max_tokens=200,
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
    print(generate_query("Hello, how are you?", "You are an assistant that helps users with their questions. Make the answers concise and informative."))
