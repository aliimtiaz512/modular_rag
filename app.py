import streamlit as st
from orchestor import orchestrate_query
from memory import clear_memory

st.set_page_config(page_title="Modular RAG Q&A", layout="wide")

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Rizvi International Impex Q&A Portal")
st.markdown("Ask questions, explore themes, and analyze characters from **Rizvi International Impex**.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your documents …"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Processing your query..."):
        # The orchestrate_query function handles routing, extraction, and generation.
        # It currently returns a string directly.
        answer = orchestrate_query(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    st.markdown("**About this App:**")
    st.markdown("This system evaluates your query first. If it's clear, it retrieves the answer from internal documents or web scraping. Otherwise, it helps refine your question.")
    st.markdown("---")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        clear_memory(True)
        st.rerun()