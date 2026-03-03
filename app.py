import streamlit as st
import os
from orchestor import orchestrate_query
from memory import clear_memory

st.set_page_config(
    page_title="Rizvi International Impex Q&A",
    layout="wide",
    page_icon="🏢"
)

# ── Premium Dark Theme ────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, .stApp {
        background-color: #0d1117;
        font-family: 'Inter', sans-serif;
        color: #e6edf3;
    }

    /* Gradient title */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px !important;
    }

    /* Subtitle text */
    h1 + div p { color: #8b949e !important; font-size: 1rem !important; }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 14px !important;
        padding: 1.1rem 1.4rem !important;
        margin-bottom: 12px !important;
        border: 1px solid #21262d !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.25) !important;
    }

    /* User bubble */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, #161b22, #0d1117) !important;
        border-left: 3px solid #58a6ff !important;
    }

    /* Assistant bubble */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg, #1a1040, #0d1117) !important;
        border-left: 3px solid #bc8cff !important;
    }

    /* Input box */
    .stChatInputContainer {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 24px !important;
        box-shadow: 0 0 0 0 transparent !important;
        transition: border 0.2s, box-shadow 0.2s;
    }
    .stChatInputContainer:focus-within {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 3px rgba(88,166,255,0.15) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #090d13 !important;
        border-right: 1px solid #21262d !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e6edf3 !important;
        -webkit-text-fill-color: #e6edf3 !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(90deg, #1f6feb, #388bfd) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 3px 10px rgba(31,111,235,0.35) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #388bfd, #58a6ff) !important;
        box-shadow: 0 5px 18px rgba(56,139,253,0.5) !important;
        transform: translateY(-1px);
    }

    /* General text */
    p, li, label { color: #c9d1d9 !important; }

    /* Spinner */
    .stSpinner > div { border-top-color: #58a6ff !important; }

    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── App Layout ───────────────────────────────────────────────────────────────
st.title("🏢 Rizvi International Impex")
st.markdown("Ask anything about **Rizvi International Impex** — our AI agent will find the answer for you.")

# ── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render chat history ──────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Handle new input ─────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about Rizvi International Impex…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking…"):
        answer = orchestrate_query(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🏢 Rizvi International Impex")
    st.markdown("---")
    st.markdown("#### About")
    st.markdown(
        "This AI-powered assistant uses a modular RAG pipeline to answer questions about "
        "**Rizvi International Impex** using internal documents and web data."
    )
    st.markdown("---")
    st.markdown("#### Quick Tips")
    st.markdown("- Ask about products, services, or company info\n- For external websites, paste the URL in your question\n- Answers are generated using Groq AI")
    st.markdown("---")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        clear_memory(True)
        st.rerun()