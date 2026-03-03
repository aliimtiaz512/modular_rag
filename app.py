import streamlit as st
from orchestor import orchestrate_query
from memory import clear_memory

st.set_page_config(
    page_title="Rizvi International Impex",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# ── LIGHT THEME ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* ── BASE ── */
    html, body, .stApp {
        background-color: #f5f7fa !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1e293b !important;
    }

    /* ── HIDE STREAMLIT CHROME ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── SIDEBAR TOGGLE BUTTON ── */
    [data-testid="collapsedControl"] {
        background-color: #2563eb !important;
        border-radius: 0 10px 10px 0 !important;
        border: none !important;
        box-shadow: 2px 2px 12px rgba(37,99,235,0.35) !important;
        width: 26px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="collapsedControl"]:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 2px 2px 18px rgba(37,99,235,0.55) !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }

    /* ── TITLE ── */
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        letter-spacing: -0.04em !important;
        margin-bottom: 4px !important;
    }

    h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    p, li {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #475569 !important;
        line-height: 1.7 !important;
    }

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 1.1rem 1.4rem !important;
        margin-bottom: 12px !important;
        transition: box-shadow 0.2s ease, transform 0.2s ease !important;
    }

    /* User message */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 4px solid #2563eb !important;
        box-shadow: 0 2px 12px rgba(37,99,235,0.07) !important;
    }

    /* Assistant message */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-left: 4px solid #16a34a !important;
        box-shadow: 0 2px 12px rgba(22,163,74,0.07) !important;
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08) !important;
    }

    /* ── SCROLLABLE CHAT AREA ── */
    .chat-scroll-area {
        max-height: 60vh;
        overflow-y: scroll;
        overflow-x: hidden;
        padding-right: 6px;
        scrollbar-width: thin;
        scrollbar-color: #93c5fd #e2e8f0;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track {
        background: #e2e8f0;
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #93c5fd;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }
    ::-webkit-scrollbar-thumb:hover { background: #2563eb; }

    /* ── CHAT INPUT ── */
    .stChatInputContainer {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12),
                    0 4px 16px rgba(37,99,235,0.1) !important;
    }

    textarea, input {
        background-color: transparent !important;
        color: #1e293b !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(37,99,235,0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
        transform: translateY(-1px) !important;
        color: #fff !important;
        border: none !important;
    }

    /* ── DIVIDERS ── */
    hr { border-color: #e2e8f0 !important; }

    /* ── SPINNER ── */
    .stSpinner > div { border-top-color: #2563eb !important; }

</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([8, 2])
with col1:
    st.markdown("""
    <div style="padding: 20px 0 6px 0;">
        <h1 style="margin:0;">🏢 Rizvi International Impex</h1>
        <p style="font-size:15px; margin:6px 0 0 0; color:#64748b;">
            Ask anything — powered by your internal knowledge base &amp; live web data.
        </p>
    </div>
    <hr style="margin: 16px 0 20px 0;" />
    """, unsafe_allow_html=True)

# ── CHAT STATE ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 60px 20px;
        color: #94a3b8;
    ">
        <div style="font-size: 48px; margin-bottom: 12px;">💬</div>
        <p style="font-size: 18px; font-weight: 600; color: #64748b; margin:0;">No messages yet</p>
        <p style="font-size: 14px; margin-top:6px;">Type a question below to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# Scrollable chat window
st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Ask a question about Rizvi International Impex…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking…"):
        answer = orchestrate_query(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    st.rerun()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / Brand
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border-radius: 14px;
        padding: 18px 16px;
        margin-bottom: 20px;
        text-align: center;
    ">
        <div style="font-size: 28px;">🏢</div>
        <p style="color: #fff; font-weight: 700; font-size: 15px; margin: 6px 0 2px;">Rizvi International</p>
        <p style="color: #bfdbfe; font-size: 12px; margin: 0;">AI-Powered Q&A</p>
    </div>
    """, unsafe_allow_html=True)

    msg_count = len(st.session_state.messages)

    # Stats card
    st.markdown(f"""
    <div style="
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 16px;
    ">
        <p style="font-size:12px; color:#0284c7; font-weight:600; margin:0 0 6px 0; text-transform:uppercase; letter-spacing:.05em;">Session Stats</p>
        <p style="font-size:22px; font-weight:800; color:#0c4a6e; margin:0;">{msg_count}</p>
        <p style="font-size:12px; color:#0369a1; margin:0;">messages exchanged</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <p style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 6px;">⚙️ How It Works</p>
    <p style="font-size: 12.5px; color: #64748b; line-height: 1.6;">
        Your query is intelligently routed to either the
        <strong style="color:#2563eb;">vector database</strong> or
        <strong style="color:#16a34a;">live web extraction</strong>,
        then answered by a large language model.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        clear_memory(True)
        st.rerun()

    st.markdown("""
    <p style="font-size: 11px; color: #94a3b8; text-align: center; margin-top: 24px;">
        Rizvi International Impex © 2026
    </p>
    """, unsafe_allow_html=True)