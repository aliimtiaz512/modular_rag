import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load from .env for local development
load_dotenv()

# On Streamlit Cloud, use st.secrets. Fallback to .env for local dev.
try:
    import streamlit as st
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
except Exception:
    api_key = os.getenv("OPENAI_API_KEY")


def generate_query(query: str, system_prompt: str):
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0.7,
        max_tokens=384
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("user", "{query}")
    ])

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({
        "system_prompt": system_prompt,
        "query": query
    })

    return response