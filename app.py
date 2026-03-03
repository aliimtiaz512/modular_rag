import streamlit as st
from orchestor import orchestrate_query
from memory import clear_memory

st.set_page_config(
    page_title="Rizvi International Impex",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# ── CHARCOAL + TEAL THEME ────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

    /* ── BASE ── */
    html, body, .stApp {
        background-color: #1a1a1a !important;
        font-family: 'DM Sans', sans-serif !important;
        color: #e8e8e8 !important;
    }

    /* ── HIDE STREAMLIT CHROME ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── SIDEBAR TOGGLE BUTTON ── */
    [data-testid="collapsedControl"] {
        background-color: #e2faf8 !important;
        border-radius: 0 10px 10px 0 !important;
        border: 1px solid #14b8a6 !important;
        border-left: none !important;
        box-shadow: 2px 2px 10px rgba(20,184,166,0.25) !important;
        width: 28px !important;
        top: 50% !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="collapsedControl"]:hover {
        background-color: #14b8a6 !important;
        box-shadow: 2px 2px 16px rgba(20,184,166,0.5) !important;
    }

    [data-testid="collapsedControl"] svg {
        fill: #0d9488 !important;
        stroke: #0d9488 !important;
    }

    [data-testid="collapsedControl"]:hover svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }
    /* ── TITLE ── */
    h1 {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        color: #f0f0f0 !important;
        border-left: 4px solid #14b8a6;
        padding-left: 16px !important;
        margin-bottom: 6px !important;
    }

    h2, h3, h4 {
        font-family: 'DM Sans', sans-serif !important;
        color: #e0e0e0 !important;
        font-weight: 600 !important;
    }

    p, li {
        color: #b0b0b0 !important;
        font-family: 'DM Sans', sans-serif !important;
        line-height: 1.7 !important;
    }

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {
        border-radius: 14px !important;
        padding: 1.1rem 1.4rem !important;
        margin-bottom: 12px !important;
        transition: box-shadow 0.2s ease !important;
    }

    /* User message — warm amber accent */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #252525 !important;
        border: 1px solid #333 !important;
        border-top: 3px solid #f59e0b !important;
        box-shadow: 0 2px 12px rgba(245,158,11,0.08) !important;
    }

    /* Assistant message — teal accent */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #222 !important;
        border: 1px solid #2e2e2e !important;
        border-top: 3px solid #14b8a6 !important;
        box-shadow: 0 2px 12px rgba(20,184,166,0.08) !important;
    }

    [data-testid="stChatMessage"]:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.35) !important;
    }

    /* ── CHAT INPUT ── */
    .stChatInputContainer {
        background-color: #252525 !important;
        border: 1px solid #404040 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25) !important;
    }

    .stChatInputContainer:focus-within {
        border-color: #14b8a6 !important;
        box-shadow: 0 4px 20px rgba(20,184,166,0.2) !important;
    }

    textarea, input {
        background-color: transparent !important;
        color: #e8e8e8 !important;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background-color: #141414 !important;
        border-right: 1px solid #2e2e2e !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        background-color: #14b8a6 !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(20,184,166,0.3) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #0d9488 !important;
        box-shadow: 0 6px 22px rgba(20,184,166,0.45) !important;
        transform: translateY(-1px) !important;
        color: #fff !important;
        border: none !important;
    }

    /* ── DIVIDERS ── */
    hr {
        border-color: #2e2e2e !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #1a1a1a; }
    ::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #14b8a6; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.title("🤖 Rizvi International Impex")
st.markdown(
    "<p style='font-size:15px; margin-top:-4px; margin-bottom:28px;'>"
    "Ask anything — powered by your internal knowledge base &amp; live web data."
    "</p>",
    unsafe_allow_html=True
)

# ── CHAT STATE ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about Rizvi International Impex…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking…"):
        answer = orchestrate_query(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='font-size:17px; color:#e0e0e0 !important; margin-bottom:4px;'>🛠 Controls</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    msg_count = len(st.session_state.messages)
    st.markdown(
        f"<p style='font-size:13px;'>💬 Messages this session: "
        f"<strong style='color:#14b8a6;'>{msg_count}</strong></p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown(
        "<p style='font-size:13px;'><strong style='color:#e0e0e0;'>How it works</strong><br>"
        "Your query is routed to either the vector database or live web extraction, "
        "then answered by an LLM.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        clear_memory(True)
        st.rerun()

    st.markdown(
        "<p style='font-size:11px; color:#555; margin-top:20px; text-align:center;'>"
        "Rizvi International Impex © 2026</p>",
        unsafe_allow_html=True
    )