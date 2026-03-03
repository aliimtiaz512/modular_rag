import streamlit as st
from orchestor import orchestrate_query
from memory import clear_memory

st.set_page_config(
    page_title="Rizvi International Impex",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="collapsed"   # sidebar closed by default; arrow shows on left edge
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

    /* Hide clutter but NOT the sidebar arrow toggle */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    [data-testid="stToolbar"]     { display: none; }
    [data-testid="stDecoration"]  { display: none; }
    [data-testid="stStatusWidget"]{ display: none; }

    /* ── Native sidebar toggle — large dark pill on the left edge ── */
    [data-testid="collapsedControl"] {
        display:          flex         !important;
        visibility:       visible      !important;
        opacity:          1            !important;
        background-color: #1e293b     !important;   /* dark charcoal */
        border-radius:    0 14px 14px 0 !important;
        border:           none         !important;
        box-shadow:       3px 0 18px rgba(0,0,0,0.25) !important;
        width:            36px         !important;
        min-height:       64px         !important;
        align-items:      center       !important;
        justify-content:  center       !important;
        transition:       all 0.2s ease !important;
        cursor:           pointer      !important;
        z-index:          9999         !important;
        position:         fixed        !important;
        top:              50%          !important;
        left:             0            !important;
        transform:        translateY(-50%) !important;
    }
    [data-testid="collapsedControl"]:hover {
        background-color: #0f172a !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
        width: 40px !important;
    }
    [data-testid="collapsedControl"] svg {
        fill:   #ffffff !important;
        stroke: #ffffff !important;
        width:  18px    !important;
        height: 18px    !important;
    }

    /* ── Title ── */
    h1 {
        font-weight: 800 !important;
        color: #1e293b !important;
        letter-spacing: -0.04em !important;
        font-size: 2rem !important;
        margin-bottom: 4px !important;
    }
    h2, h3, h4 { color: #1e293b !important; font-weight: 700 !important; }
    p, li { color: #475569 !important; line-height: 1.7 !important; }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        border-radius:  16px !important;
        padding:        1.1rem 1.4rem !important;
        margin-bottom:  12px !important;
        transition:     box-shadow 0.2s ease, transform 0.2s ease !important;
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #ffffff !important;
        border:     1px solid #e2e8f0 !important;
        border-left: 4px solid #2563eb !important;
        box-shadow: 0 2px 12px rgba(37,99,235,0.07) !important;
    }
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #f0fdf4 !important;
        border:     1px solid #bbf7d0 !important;
        border-left: 4px solid #16a34a !important;
        box-shadow: 0 2px 12px rgba(22,163,74,0.07) !important;
    }
    [data-testid="stChatMessage"]:hover {
        transform:  translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08) !important;
    }

    /* ── Scrollable chat container ── */
    .chat-box {
        max-height:     60vh;
        overflow-y:     scroll;
        overflow-x:     hidden;
        padding-right:  6px;
        scrollbar-width: thin;
        scrollbar-color: #93c5fd #e2e8f0;
    }
    ::-webkit-scrollbar       { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #e2e8f0; border-radius: 8px; }
    ::-webkit-scrollbar-thumb { background: #93c5fd; border-radius: 8px; border: 2px solid #e2e8f0; }
    ::-webkit-scrollbar-thumb:hover { background: #2563eb; }

    /* ── Chat input ── */
    .stChatInputContainer {
        background-color: #ffffff   !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 16px         !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12), 0 4px 16px rgba(37,99,235,0.1) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #ffffff   !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 2px 0 16px rgba(0,0,0,0.06) !important;
    }

    /* ── All buttons default ── */
    .stButton > button {
        font-family:      'Plus Jakarta Sans', sans-serif !important;
        background-color: #2563eb  !important;
        color:            #ffffff  !important;
        border:           none     !important;
        border-radius:    10px     !important;
        padding:          10px 20px !important;
        font-weight:      600      !important;
        font-size:        14px     !important;
        width:            100%     !important;
        box-shadow:       0 4px 14px rgba(37,99,235,0.3) !important;
        transition:       all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
        transform:  translateY(-1px) !important;
        color: #fff !important;
        border: none !important;
    }

    /* ── Clear-chat (danger) button override ── */
    .danger-btn .stButton > button {
        background-color: #ef4444 !important;
        box-shadow: 0 4px 14px rgba(239,68,68,0.3) !important;
    }
    .danger-btn .stButton > button:hover {
        background-color: #dc2626 !important;
        box-shadow: 0 6px 20px rgba(239,68,68,0.45) !important;
    }

    hr { border-color: #e2e8f0 !important; }
    .stSpinner > div { border-top-color: #2563eb !important; }
    .stExpander { border: 1px solid #e2e8f0 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 18px 0 6px 0;">
    <h1>🏢 Rizvi International Impex</h1>
    <p style="font-size:15px; margin:4px 0 0; color:#64748b;">
        Ask anything — powered by your internal knowledge base &amp; live web data.
    </p>
</div>
<hr style="margin: 14px 0 20px;" />
""", unsafe_allow_html=True)

# ── CHAT STATE ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding:60px 20px; color:#94a3b8;">
        <div style="font-size:52px; margin-bottom:10px;">💬</div>
        <p style="font-size:18px; font-weight:600; color:#64748b; margin:0;">No messages yet</p>
        <p style="font-size:14px; margin-top:6px; color:#94a3b8;">
            Click the <strong style="color:#1e293b;">dark arrow ◀ on the left edge</strong> to open the menu,
            then type a question below.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Scrollable chat window
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

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:

    # Brand card
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border-radius: 14px; padding: 20px 16px;
        margin-bottom: 18px; text-align: center;
    ">
        <div style="font-size:32px; margin-bottom:6px;">🏢</div>
        <p style="color:#fff; font-weight:700; font-size:16px; margin:0 0 2px;">Rizvi International Impex</p>
        <p style="color:#bfdbfe; font-size:12px; margin:0; letter-spacing:0.5px;">AI-Powered Knowledge Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    # Live stats
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    ai_msgs   = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    st.markdown(f"""
    <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:12px; padding:14px 16px; margin-bottom:14px;">
        <p style="font-size:11px; color:#0284c7; font-weight:700; margin:0 0 10px; text-transform:uppercase; letter-spacing:.08em;">📊 Session Stats</p>
        <div style="display:flex; gap:8px;">
            <div style="flex:1; text-align:center; background:#e0f2fe; border-radius:8px; padding:8px;">
                <p style="font-size:22px; font-weight:800; color:#0c4a6e; margin:0;">{user_msgs}</p>
                <p style="font-size:10px; color:#0369a1; margin:0;">You asked</p>
            </div>
            <div style="flex:1; text-align:center; background:#dcfce7; border-radius:8px; padding:8px;">
                <p style="font-size:22px; font-weight:800; color:#14532d; margin:0;">{ai_msgs}</p>
                <p style="font-size:10px; color:#16a34a; margin:0;">AI replied</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Expandable info sections
    with st.expander("📖 About This System"):
        st.markdown("""
        This is a **Modular RAG** *(Retrieval-Augmented Generation)* system
        built for **Rizvi International Impex**.

        It combines a private **ChromaDB** vector knowledge base with
        **live web scraping** to give intelligent, accurate answers
        about the company and any website you share.
        """)

    with st.expander("⚙️ How It Works"):
        st.markdown("""
        1. 🔵 **Router** — Classifies your query type
        2. 🟣 **Retriever** — Fetches context from ChromaDB or scrapes a URL
        3. 🟢 **Generator** — Groq LLM composes your answer
        4. 🟡 **Memory** — Remembers past Q&As in this session
        """)

    with st.expander("✅ What I Can Do"):
        st.markdown("""
        - Answer questions about Rizvi International Impex
        - Scrape & summarize any website URL you share
        - Remember your conversation for follow-up questions
        - Route complex queries to the right data source automatically
        """)

    with st.expander("💡 Tips for Best Results"):
        st.markdown("""
        - Be specific: *"What products does Rizvi export?"*
        - Paste a full URL to scrape any site for context
        - Short, focused questions get the best answers
        - Clear chat history to start a fresh session
        """)

    st.markdown("---")

    # Clear chat — styled as danger (red) button
    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        clear_memory(True)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:11px; color:#94a3b8; text-align:center; margin-top:20px;">
        Rizvi International Impex © 2026
    </p>
    """, unsafe_allow_html=True)