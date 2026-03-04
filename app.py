import streamlit as st
from orchestor import orchestrate_query
from memory import clear_memory

st.set_page_config(
    page_title="Rizvi International Impex",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="collapsed"
)

# ── LIGHT THEME ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, .stApp {
        background-color: #f5f7fa !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1e293b !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    h1 {
        font-weight: 800 !important;
        color: #1e293b !important;
        letter-spacing: -0.04em !important;
        font-size: 2rem !important;
        margin-bottom: 4px !important;
    }
    h2, h3, h4 { color: #1e293b !important; font-weight: 700 !important; }
    p, li { color: #475569 !important; line-height: 1.7 !important; }

    /* ── Expander (Menu panel) ── */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
        margin-bottom: 20px !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 700 !important;
        font-size: 15px !important;
        color: #1e293b !important;
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 1.1rem 1.4rem !important;
        margin-bottom: 12px !important;
        transition: box-shadow 0.2s ease, transform 0.2s ease !important;
    }
    
    /* User Message (odd) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 4px solid #334155 !important; /* Slate 700 */
        box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
    }
    
    /* AI Response (even) */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f5f3ff !important; /* Premium subtle violet */
        border: 1px solid #ede9fe !important;
        border-left: 4px solid #8b5cf6 !important; /* Violet 500 */
        box-shadow: 0 2px 12px rgba(139,92,246,0.08) !important;
    }
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08) !important;
    }

    /* ── Scrollable chat area ── */
    .chat-box {
        max-height: 60vh;
        overflow-y: scroll;
        overflow-x: hidden;
        padding-right: 6px;
        scrollbar-width: thin;
        scrollbar-color: #93c5fd #e2e8f0;
    }
    ::-webkit-scrollbar       { width: 8px; }
    ::-webkit-scrollbar-track { background: #e2e8f0; border-radius: 8px; }
    ::-webkit-scrollbar-thumb { background: #93c5fd; border-radius: 8px; border: 2px solid #e2e8f0; }
    ::-webkit-scrollbar-thumb:hover { background: #2563eb; }

    /* ── Chat input ── */
    .stChatInputContainer {
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
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

    hr { border-color: #e2e8f0 !important; }
    .stSpinner > div { border-top-color: #2563eb !important; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 18px 0 6px 0;">
    <h1>🏢 Rizvi International Impex</h1>
    <p style="font-size:15px; margin:4px 0 0; color:#64748b;">
        AI-powered Q&amp;A — knowledge base &amp; live web data.
    </p>
</div>
""", unsafe_allow_html=True)

# ── MENU PANEL (replaces sidebar — always visible, click to expand) ──────────
with st.expander("☰  Menu — Settings & Info", expanded=False):

    # Stats row
    if "messages" in st.session_state:
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        ai_msgs   = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    else:
        user_msgs = ai_msgs = 0

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:12px; padding:14px; text-align:center;">
            <p style="font-size:24px; font-weight:800; color:#0c4a6e; margin:0;">{user_msgs}</p>
            <p style="font-size:12px; color:#0369a1; margin:0;">You asked</p>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:14px; text-align:center;">
            <p style="font-size:24px; font-weight:800; color:#14532d; margin:0;">{ai_msgs}</p>
            <p style="font-size:12px; color:#16a34a; margin:0;">AI replied</p>
        </div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div style="background:#fefce8; border:1px solid #fde68a; border-radius:12px; padding:14px; text-align:center;">
            <p style="font-size:24px; font-weight:800; color:#713f12; margin:0;">{user_msgs + ai_msgs}</p>
            <p style="font-size:12px; color:#92400e; margin:0;">Total messages</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    info_col, tips_col = st.columns(2)
    with info_col:
        st.markdown("**📖 About This System**")
        st.markdown("""
        This is a **Modular RAG** *(Retrieval-Augmented Generation)* system for
        **Rizvi International Impex**. It combines a private **ChromaDB** vector
        knowledge base with **live web scraping** to answer questions intelligently.
        """)
        st.markdown("**⚙️ How It Works**")
        st.markdown("""
        1. 🔵 **Router** — Classifies your query  
        2. 🟣 **Retriever** — Fetches from ChromaDB or scrapes a URL  
        3. 🟢 **Generator** — Groq LLM writes the answer  
        4. 🟡 **Memory** — Remembers session context
        """)
    with tips_col:
        st.markdown("**✅ What I Can Do**")
        st.markdown("""
        - Answer questions about Rizvi International Impex  
        - Scrape & summarize any website URL  
        - Remember follow-up context within a session  
        - Route queries to the right data source automatically
        """)
        st.markdown("**💡 Tips for Best Results**")
        st.markdown("""
        - Be specific: *"Tell me about rizvi's?"*  
        - Paste a full URL to scrape any website  
        - Short, focused questions get the best answers  
        - Clear chat to start fresh
        """)

    st.markdown("---")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        clear_memory(True)
        st.rerun()

st.markdown("<hr style='margin: 0 0 20px;'>", unsafe_allow_html=True)

# ── CHAT STATE ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding:50px 20px;">
        <div style="font-size:52px; margin-bottom:10px;">💬</div>
        <p style="font-size:18px; font-weight:600; color:#64748b; margin:0;">No messages yet</p>
        <p style="font-size:14px; margin-top:6px; color:#94a3b8;">Type a question below to get started.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="chat-box">', unsafe_allow_html=True)
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