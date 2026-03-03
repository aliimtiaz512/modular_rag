import streamlit as st
from orchestor import orchestrate_query
from memory import clear_memory

st.set_page_config(
    page_title="Rizvi International Impex",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="expanded"
)

# ── ADVANCED DARK THEME ─────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    /* ── ROOT / BODY ── */
    :root {
        --bg-base:        #05071a;
        --bg-surface:     #0d1330;
        --bg-card:        #111827;
        --accent-blue:    #4f8eff;
        --accent-violet:  #a78bfa;
        --accent-cyan:    #22d3ee;
        --accent-emerald: #10b981;
        --text-primary:   #f1f5f9;
        --text-muted:     #94a3b8;
        --border:         rgba(255,255,255,0.06);
    }

    html, body, .stApp {
        background-color: var(--bg-base) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* Subtle animated star-like dot grid background */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(circle at 20% 30%, rgba(79,142,255,0.07) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(167,139,250,0.07) 0%, transparent 50%),
            radial-gradient(circle at 50% 90%, rgba(16,185,129,0.05) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }

    /* ── HIDE STREAMLIT CHROME ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── TITLE / HERO AREA ── */
    h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.04em !important;
        background: linear-gradient(100deg, #4f8eff 10%, #a78bfa 45%, #22d3ee 80%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 4px !important;
        padding-top: 10px !important;
    }

    h2, h3, h4, h5 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    p, li, span {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-muted) !important;
        line-height: 1.7 !important;
    }

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {
        padding: 1.2rem 1.5rem !important;
        border-radius: 18px !important;
        margin-bottom: 14px !important;
        border: 1px solid var(--border) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4) !important;
    }

    /* User message — blue tinted */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg,
            rgba(79,142,255,0.12) 0%,
            rgba(13,19,48,0.85) 100%) !important;
        border-left: 3px solid var(--accent-blue) !important;
        box-shadow: 0 4px 20px rgba(79,142,255,0.06), inset 0 0 0 1px rgba(79,142,255,0.1) !important;
    }

    /* Assistant message — violet tinted */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(135deg,
            rgba(167,139,250,0.10) 0%,
            rgba(13,19,48,0.85) 100%) !important;
        border-left: 3px solid var(--accent-violet) !important;
        box-shadow: 0 4px 20px rgba(167,139,250,0.06), inset 0 0 0 1px rgba(167,139,250,0.1) !important;
    }

    /* ── CHAT INPUT ── */
    .stChatInputContainer {
        background: rgba(13,19,48,0.8) !important;
        border: 1px solid rgba(79,142,255,0.25) !important;
        border-radius: 24px !important;
        box-shadow: 0 0 0 4px rgba(79,142,255,0.04),
                    0 8px 32px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(16px) !important;
        padding: 6px 10px !important;
        transition: all 0.3s ease !important;
    }

    .stChatInputContainer:focus-within {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 4px rgba(79,142,255,0.15),
                    0 8px 40px rgba(79,142,255,0.2) !important;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080c1f 0%, #0a0f24 100%) !important;
        border-right: 1px solid rgba(79,142,255,0.12) !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: var(--text-muted) !important;
    }

    /* Sidebar metric/badge style for stats */
    .sidebar-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        font-family: 'Space Grotesk', sans-serif !important;
        background: linear-gradient(135deg, #4f8eff, #7c3aed) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 11px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(79,142,255,0.35) !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #6fa3ff, #9d5cf0) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(79,142,255,0.5) !important;
        color: #fff !important;
        border: none !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── DIVIDERS ── */
    hr {
        border-color: rgba(255,255,255,0.06) !important;
        margin: 16px 0 !important;
    }

    /* ── SPINNER ── */
    .stSpinner > div {
        border-top-color: var(--accent-blue) !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(79,142,255,0.3);
        border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ─────────────────────────────────────────────────────────────
st.title("🌐 Rizvi International Impex")
st.markdown(
    "<p style='font-size:16px; margin-top:-8px; margin-bottom:24px;'>"
    "Intelligent Q&amp;A powered by your documents &amp; live web data."
    "</p>",
    unsafe_allow_html=True
)

# ── CHAT STATE ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle new input
if prompt := st.chat_input("Ask anything about Rizvi International Impex…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking…"):
        answer = orchestrate_query(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='font-size:18px; color:#f1f5f9 !important; margin-bottom:4px;'>⚙️ Controls</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Stats
    msg_count = len(st.session_state.messages)
    st.markdown(
        f"<p style='font-size:13px;'>💬 Messages in session: "
        f"<strong style='color:#4f8eff;'>{msg_count}</strong></p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(
        "<p style='font-size:13px;'><strong style='color:#f1f5f9;'>How it works:</strong><br>"
        "Your query is routed intelligently — either to the internal "
        "knowledge base or to live web extraction — then answered by an LLM.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        clear_memory(True)
        st.rerun()

    st.markdown(
        "<p style='font-size:11px; color:#475569; margin-top:20px; text-align:center;'>"
        "Rizvi International Impex © 2026</p>",
        unsafe_allow_html=True
    )