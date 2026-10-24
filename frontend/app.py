import streamlit as st
import requests
import uuid
import time

# ─── Configuration ────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DocuMind — AI Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Premium Dark Theme CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Palette ────────────────────────────────────────────────────────── */
:root {
    --bg-primary:    #0B0F1A;
    --bg-secondary:  #111827;
    --bg-card:       rgba(17, 24, 39, 0.65);
    --border:        rgba(99, 102, 241, 0.18);
    --border-hover:  rgba(99, 102, 241, 0.45);
    --accent:        #6366F1;
    --accent-light:  #818CF8;
    --accent-glow:   rgba(99, 102, 241, 0.35);
    --success:       #34D399;
    --warning:       #FBBF24;
    --danger:        #F87171;
    --text-primary:  #F1F5F9;
    --text-secondary:#94A3B8;
    --text-muted:    #64748B;
    --gradient-start:#6366F1;
    --gradient-end:  #A855F7;
}

/* ── Global Resets ───────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], .main,
[data-testid="stApp"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E1B4B 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: var(--bg-secondary);
    border-radius: 14px;
    padding: 6px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-weight: 600 !important;
    font-size: 1.00rem !important;
    color: var(--text-secondary) !important;
    transition: all 0.25s ease !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: rgba(99,102,241,0.08) !important;
}
# .stTabs [aria-selected="true"] {
#     background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
#     color: #fff !important;
#     box-shadow: 0 4px 15px var(--accent-glow) !important;
# }

.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 1.00rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px var(--accent-glow) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px var(--accent-glow) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Inputs / Selects ────────────────────────────────────────────────────── */
.stTextInput > div > div,
.stNumberInput > div > div,
.stSelectbox > div > div,
.stFileUploader > div {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    transition: border 0.2s ease !important;
}
.stTextInput > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stSelectbox > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
input, textarea { color: var(--text-primary) !important; }
label { color: var(--text-secondary) !important; }

/* ── Chat Messages ───────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    margin-bottom: 12px !important;
}

/* ── Expanders ───────────────────────────────────────────────────────────── */
details {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(12px) !important;
}
details summary {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ── Glass Card ──────────────────────────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 16px;
    transition: border 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    border-color: var(--border-hover);
    box-shadow: 0 8px 30px rgba(99,102,241,0.10);
}

/* ── Flashcard ───────────────────────────────────────────────────────────── */
.flashcard-container {
    perspective: 1200px;
    min-height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 24px 0;
}
.flashcard-face {
    background: linear-gradient(145deg, rgba(99,102,241,0.12), rgba(168,85,247,0.08));
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 40px 36px;
    text-align: center;
    width: 100%;
    max-width: 650px;
    margin: 0 auto;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}
.flashcard-face:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(99,102,241,0.18);
}
.flashcard-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-light);
    margin-bottom: 16px;
}
.flashcard-text {
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--text-primary);
    line-height: 1.6;
}
.card-counter {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 8px;
}
.card-progress {
    height: 4px;
    background: var(--bg-secondary);
    border-radius: 2px;
    overflow: hidden;
    max-width: 650px;
    margin: 0 auto 20px;
}
.card-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    border-radius: 2px;
    transition: width 0.4s ease;
}

/* ── Quiz Option Cards ───────────────────────────────────────────────────── */
.quiz-question-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.quiz-question-num {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-light);
    margin-bottom: 8px;
}
.quiz-question-text {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
}

/* ── Metric Stat Cards ───────────────────────────────────────────────────── */
.stat-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
}
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

/* ── Topic Card ──────────────────────────────────────────────────────────── */
.topic-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}
.topic-card:hover {
    border-color: var(--border-hover);
    transform: translateX(4px);
}
.topic-name {
    font-size: 1rem;
    font-weight: 700;
    color: var(--accent-light);
    margin-bottom: 6px;
}
.topic-desc {
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ── Notes Container ─────────────────────────────────────────────────────── */
.notes-container {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 36px;
    line-height: 1.75;
}
.notes-container h1, .notes-container h2, .notes-container h3 {
    color: var(--accent-light) !important;
    margin-top: 24px;
}
.notes-container p, .notes-container li {
    color: var(--text-secondary);
}

/* ── Dividers ────────────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 16px 0 !important;
}

/* ── Score Ring ───────────────────────────────────────────────────────────── */
.score-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    font-size: 2.2rem;
    font-weight: 800;
    color: #fff;
}
.score-great { background: conic-gradient(var(--success) var(--pct), var(--bg-secondary) 0); }
.score-ok    { background: conic-gradient(var(--warning) var(--pct), var(--bg-secondary) 0); }
.score-low   { background: conic-gradient(var(--danger)  var(--pct), var(--bg-secondary) 0); }
.score-inner {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: var(--bg-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Hero Header ─────────────────────────────────────────────────────────── */
.hero-header {
    text-align: center;
    padding: 48px 20px 24px;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-muted);
    font-weight: 400;
}

/* ── Empty State ─────────────────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 80px 20px;
}
.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 16px;
    opacity: 0.6;
}
.empty-state-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.empty-state-desc {
    font-size: 0.92rem;
    color: var(--text-muted);
}

/* ── Upload Success Badge ────────────────────────────────────────────────── */
.upload-badge {
    background: rgba(52, 211, 153, 0.12);
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 12px;
    text-align: center;
}
.upload-badge-text {
    color: var(--success);
    font-weight: 600;
    font-size: 0.88rem;
}

/* ── Sidebar Doc Info ────────────────────────────────────────────────────── */
.doc-info-chip {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 0.78rem;
    color: var(--accent-light);
    margin-top: 8px;
    word-break: break-all;
}

/* ── Animations ──────────────────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in {
    animation: fadeInUp 0.5s ease-out forwards;
}

/* ── Scrollbar ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--accent);
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Initialization ─────────────────────────────────────────────
defaults = {
    "session_id": str(uuid.uuid4()),
    "documents": {},          # {doc_id: {filename, title, chunks_size, file_size}}
    "active_doc_id": None,
    "chat_history": [],
    "flashcards": [],
    "flashcard_idx": 0,
    "show_card_answer": False,
    "notes_content": None,
    "topics_list": None,
    "quiz_questions": None,
    "quiz_submitted": False,
    "quiz_answers": {},
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0px 0 5px;">
        <div style="font-size:3.2rem;">🧠</div>
        <div style="font-size:3.0rem; font-weight:800;
            background: linear-gradient(135deg, #6366F1, #A855F7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;">DocuMind</div>
        <div style="font-size:0.81rem; color:#64748B; margin-top:2px;">
            AI-Powered Document Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Upload Section ───────────────────────────────────────────────────────
    st.markdown("## 📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        if st.button("⚡ Ingest Document", type="primary", use_container_width=True):
            with st.spinner("Parsing, chunking & embedding…"):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    res = requests.post(f"{BACKEND_URL}/documents/upload", files=files)
                    if res.status_code == 200:
                        data = res.json()
                        doc_id = data["document_id"]
                        st.session_state["documents"][doc_id] = {
                            "filename": data["filename"],
                            "title": data.get("title", data["filename"]),
                            "chunks_size": data.get("chunks_size", 0),
                            "file_size": data.get("file_size", 0),
                        }
                        st.session_state["active_doc_id"] = doc_id
                        # Reset downstream state for new doc
                        st.session_state["chat_history"] = []
                        st.session_state["notes_content"] = None
                        st.session_state["topics_list"] = None
                        st.session_state["quiz_questions"] = None
                        st.session_state["flashcards"] = []
                        st.markdown(f"""
                        <div class="upload-badge">
                            <div class="upload-badge-text">
                                ✅ {data['filename']} processed — {data.get('chunks_size',0)} chunks
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Upload failed. Check backend logs.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Is the server running?")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ── Document Selector ────────────────────────────────────────────────────
    if st.session_state["documents"]:
        st.divider()
        st.markdown("### 📚 Active Document")
        doc_options = list(st.session_state["documents"].keys())
        selected_id = st.selectbox(
            "Select Document",
            options=doc_options,
            format_func=lambda x: st.session_state["documents"][x]["filename"],
            index=doc_options.index(st.session_state["active_doc_id"])
            if st.session_state["active_doc_id"] in doc_options else 0,
            label_visibility="collapsed",
        )
        st.session_state["active_doc_id"] = selected_id

        doc_meta = st.session_state["documents"][selected_id]
        size_kb = doc_meta["file_size"] / 1024
        size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb / 1024:.1f} MB"
        st.markdown(f"""
        <div class="doc-info-chip">
            📄 <b>{doc_meta['filename']}</b><br/>
            🧩 {doc_meta['chunks_size']} chunks &nbsp;·&nbsp; 📦 {size_str}
        </div>
        """, unsafe_allow_html=True)

    # ── Session Footer ───────────────────────────────────────────────────────
    st.divider()
    st.caption(f"🔑 Session `{st.session_state['session_id'][:8]}…`")


# ─── Main Area ────────────────────────────────────────────────────────────────
if not st.session_state["active_doc_id"]:
    st.markdown("""
    <div class="hero-header animate-in">
        <div class="hero-title">DocuMind Workspace</div>
        <div class="hero-subtitle">
            Upload a PDF to unlock AI-powered Q&A, study notes, flashcards, quizzes & more
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    cols = st.columns(3)
    features = [
        ("💬", "Chat Q&A", "Ask questions and get instant, context-aware answers from your document."),
        ("📝", "Auto Notes", "AI summarizes your entire document into structured study notes."),
        ("🗂️", "Topics", "Automatically discover and organize the key topics in your document."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="glass-card animate-in" style="text-align:center; min-height:180px;">
                <div style="font-size:2.2rem; margin-bottom:10px;">{icon}</div>
                <div style="font-size:1rem; font-weight:700; color:var(--text-primary); margin-bottom:6px;">{title}</div>
                <div style="font-size:0.84rem; color:var(--text-muted);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    cols2 = st.columns(3)
    features2 = [
        ("🃏", "Flashcards", "Generate interactive study flashcards to test your understanding."),
        ("❓", "Quiz", "Build multiple-choice assessments with instant auto-grading."),
        ("🚀", "RAG Pipeline", "Powered by retrieval-augmented generation for accurate answers."),
    ]
    for col, (icon, title, desc) in zip(cols2, features2):
        with col:
            st.markdown(f"""
            <div class="glass-card animate-in" style="text-align:center; min-height:180px;">
                <div style="font-size:2.2rem; margin-bottom:10px;">{icon}</div>
                <div style="font-size:1rem; font-weight:700; color:var(--text-primary); margin-bottom:6px;">{title}</div>
                <div style="font-size:0.84rem; color:var(--text-muted);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:32px;">
        <div style="font-size:0.8rem; color:var(--text-muted);">
            👈 Upload a PDF from the sidebar to get started
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    active_doc_id = st.session_state["active_doc_id"]
    active_doc = st.session_state["documents"][active_doc_id]
    active_doc_name = active_doc["filename"]

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom: 8px;">
        <span style="font-size:2.8rem; font-weight:800;
            background: linear-gradient(135deg, #6366F1, #A855F7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;">DocuMind Workspace</span>
        <span style="font-size:0.82rem; color:var(--text-muted); margin-left:12px;">
            📄 {active_doc_name}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_chat, tab_notes, tab_topics, tab_cards, tab_quiz = st.tabs([
        "💬 Chat Q&A",
        "📝 Study Notes",
        "🗂️ Topics",
        "🃏 Flashcards",
        "❓ Quiz",
    ])

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 1 — CONVERSATIONAL Q&A
    # ═════════════════════════════════════════════════════════════════════════
    with tab_chat:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:20px;">
            <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
                💬 Ask Anything About Your Document
            </div>
            <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
                Powered by RAG — your questions are answered using relevant document chunks.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Display chat messages
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if user_prompt := st.chat_input("Ask a question about the document…"):
            st.session_state["chat_history"].append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            with st.chat_message("assistant"):
                with st.spinner("Retrieving context & generating response…"):
                    payload = {
                        "session_id": st.session_state["session_id"],
                        "document_id": active_doc_id,
                        "question": user_prompt,
                    }
                    try:
                        res = requests.post(f"{BACKEND_URL}/chats/chat", json=payload)
                        if res.status_code == 200:
                            answer = res.json().get("answer", "No response received.")
                            st.markdown(answer)
                            st.session_state["chat_history"].append(
                                {"role": "assistant", "content": answer}
                            )
                        else:
                            st.error("Failed to fetch response from backend.")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to backend. Is the server running?")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 2 — STUDY NOTES
    # ═════════════════════════════════════════════════════════════════════════
    with tab_notes:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:20px;">
            <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
                📝 AI-Generated Study Notes
            </div>
            <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
                Uses a map-reduce chain to summarize each chunk, then synthesize comprehensive notes.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Generate Study Notes", type="primary", use_container_width=False):
            with st.spinner("Summarizing document chunks — this may take a moment…"):
                try:
                    res = requests.post(f"{BACKEND_URL}/notes/{active_doc_id}")
                    if res.status_code == 200:
                        st.session_state["notes_content"] = res.json().get("notes", "")
                    else:
                        st.error("Failed to generate notes.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend.")
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state["notes_content"]:
            st.markdown(
                f'<div class="notes-container animate-in">{st.session_state["notes_content"]}</div>',
                unsafe_allow_html=True,
            )
            # Render the markdown properly too (for headers, lists, etc.)
            with st.expander("📖 View as Markdown", expanded=False):
                st.markdown(st.session_state["notes_content"])
            st.download_button(
                "⬇️ Download Notes (.md)",
                st.session_state["notes_content"],
                file_name=f"{active_doc_name}_notes.md",
                use_container_width=False,
            )
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <div class="empty-state-title">No notes generated yet</div>
                <div class="empty-state-desc">Click "Generate Study Notes" to create AI-powered summaries.</div>
            </div>
            """, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 3 — TOPIC EXTRACTION
    # ═════════════════════════════════════════════════════════════════════════
    with tab_topics:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:20px;">
            <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
                🗂️ Key Topics in Your Document
            </div>
            <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
                AI identifies and describes the main topics covered.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔍 Extract Topics", type="primary"):
            with st.spinner("Extracting key topics…"):
                try:
                    res = requests.post(f"{BACKEND_URL}/topics/{active_doc_id}")
                    if res.status_code == 200:
                        st.session_state["topics_list"] = res.json().get("topics", [])
                    else:
                        st.error("Failed to extract topics.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend.")
                except Exception as e:
                    st.error(f"Error: {e}")

        topics = st.session_state["topics_list"]
        if topics:
            # Summary stat
            st.markdown(f"""
            <div class="stat-card" style="display:inline-block; margin-bottom:20px;">
                <span class="stat-value">{len(topics)}</span>
                <span class="stat-label" style="margin-left:8px;">Topics Discovered</span>
            </div>
            """, unsafe_allow_html=True)

            for i, t in enumerate(topics):
                st.markdown(f"""
                <div class="topic-card animate-in" style="animation-delay:{i*0.06}s;">
                    <div class="topic-name">📌 {t.get('name', 'Topic')}</div>
                    <div class="topic-desc">{t.get('description', 'No description provided.')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🗂️</div>
                <div class="empty-state-title">No topics extracted yet</div>
                <div class="empty-state-desc">Click "Extract Topics" to discover the key themes.</div>
            </div>
            """, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 4 — FLASHCARDS
    # ═════════════════════════════════════════════════════════════════════════
    with tab_cards:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:20px;">
            <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
                🃏 Interactive Study Flashcards
            </div>
            <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
                Flip through AI-generated cards to test and reinforce your knowledge.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Config row
        fc1, fc2, fc3 = st.columns([2, 2, 1])
        with fc1:
            gen_mode = st.selectbox("Scope", ["full_document", "topic"], key="fc_mode")
        with fc2:
            topic_input = st.text_input(
                "Topic (if scope = topic)", value="", key="fc_topic",
                placeholder="e.g. Neural Networks"
            )
        with fc3:
            num_cards = st.number_input("Count", min_value=1, max_value=20, value=5, key="fc_count")

        if st.button("🃏 Generate Deck", type="primary"):
            with st.spinner("Generating flashcards…"):
                payload = {
                    "document_id": active_doc_id,
                    "generation_mode": gen_mode,
                    "topic": topic_input if gen_mode == "topic" else None,
                    "num_flashcards": num_cards,
                }
                try:
                    res = requests.post(f"{BACKEND_URL}/flashcards/", json=payload)
                    if res.status_code == 200:
                        st.session_state["flashcards"] = res.json().get("questions", [])
                        st.session_state["flashcard_idx"] = 0
                        st.session_state["show_card_answer"] = False
                        st.rerun()
                    else:
                        st.error("Failed to generate flashcards.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend.")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Flashcard viewer
        cards = st.session_state["flashcards"]
        if cards:
            idx = st.session_state["flashcard_idx"]
            card = cards[idx]
            progress_pct = ((idx + 1) / len(cards)) * 100

            # Counter & progress bar
            st.markdown(f"""
            <div class="card-counter">{idx + 1} / {len(cards)}</div>
            <div class="card-progress">
                <div class="card-progress-bar" style="width:{progress_pct}%;"></div>
            </div>
            """, unsafe_allow_html=True)

            # Card face
            is_answer = st.session_state["show_card_answer"]
            label = "ANSWER" if is_answer else "QUESTION"
            content = card["answer"] if is_answer else card["question"]
            topic_label = card.get("topic", "")

            st.markdown(f"""
            <div class="flashcard-container">
                <div class="flashcard-face animate-in">
                    <div class="flashcard-label">{label}{(' · ' + topic_label) if topic_label else ''}</div>
                    <div class="flashcard-text">{content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Navigation buttons
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
                    st.session_state["flashcard_idx"] -= 1
                    st.session_state["show_card_answer"] = False
                    st.rerun()
            with nav2:
                flip_label = "🔄 Show Question" if is_answer else "🔄 Reveal Answer"
                if st.button(flip_label, use_container_width=True):
                    st.session_state["show_card_answer"] = not is_answer
                    st.rerun()
            with nav3:
                if st.button("Next ➡️", use_container_width=True, disabled=(idx >= len(cards) - 1)):
                    st.session_state["flashcard_idx"] += 1
                    st.session_state["show_card_answer"] = False
                    st.rerun()
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🃏</div>
                <div class="empty-state-title">No flashcards yet</div>
                <div class="empty-state-desc">Configure options above and click "Generate Deck".</div>
            </div>
            """, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════════
    # TAB 5 — QUIZ GENERATOR
    # ═════════════════════════════════════════════════════════════════════════
    with tab_quiz:
        st.markdown("""
        <div class="glass-card" style="margin-bottom:20px;">
            <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
                ❓ Multiple Choice Assessment
            </div>
            <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
                Auto-generated quizzes with configurable difficulty and instant grading.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Config row
        qc1, qc2, qc3, qc4 = st.columns([1, 1, 1, 1])
        with qc1:
            difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], key="qz_diff")
        with qc2:
            q_mode = st.selectbox("Scope", ["full_document", "topic"], key="qz_mode")
        with qc3:
            q_topic = st.text_input(
                "Topic", value="", key="qz_topic", placeholder="(optional)"
            )
        with qc4:
            num_q = st.number_input("Questions", min_value=1, max_value=20, value=5, key="qz_count")

        if st.button("🧪 Build Quiz", type="primary"):
            with st.spinner("Constructing multiple-choice questions…"):
                payload = {
                    "document_id": active_doc_id,
                    "difficulty": difficulty,
                    "generation_mode": q_mode,
                    "topic": q_topic if q_mode == "topic" else None,
                    "num_questions": num_q,
                }
                try:
                    res = requests.post(f"{BACKEND_URL}/quiz/", json=payload)
                    if res.status_code == 200:
                        st.session_state["quiz_questions"] = res.json().get("questions", [])
                        st.session_state["quiz_submitted"] = False
                        st.session_state["quiz_answers"] = {}
                        st.rerun()
                    else:
                        st.error("Failed to generate quiz.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend.")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Quiz rendering
        questions = st.session_state["quiz_questions"]
        if questions:
            if not st.session_state["quiz_submitted"]:
                with st.form("quiz_form"):
                    user_answers = {}
                    for i, q in enumerate(questions):
                        st.markdown(f"""
                        <div class="quiz-question-card">
                            <div class="quiz-question-num">Question {i + 1} of {len(questions)}</div>
                            <div class="quiz-question-text">{q['question']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        user_answers[i] = st.radio(
                            f"Select answer for Q{i + 1}",
                            options=q["options"],
                            key=f"q_{i}",
                            label_visibility="collapsed",
                        )

                    submitted = st.form_submit_button("📊 Submit Quiz", use_container_width=True)
                    if submitted:
                        st.session_state["quiz_answers"] = user_answers
                        st.session_state["quiz_submitted"] = True
                        st.rerun()
            else:
                # Show results
                user_answers = st.session_state["quiz_answers"]
                score = 0
                total = len(questions)

                for i, q in enumerate(questions):
                    selected = user_answers.get(i, "")
                    correct_letter = q["correct_answer"]
                    correct_option = (
                        q["options"]["ABCD".index(correct_letter)]
                        if len(correct_letter) == 1 and correct_letter in "ABCD"
                        else correct_letter
                    )
                    is_correct = selected == correct_option
                    if is_correct:
                        score += 1

                    border_color = "var(--success)" if is_correct else "var(--danger)"
                    icon = "✅" if is_correct else "❌"

                    st.markdown(f"""
                    <div class="quiz-question-card" style="border-color:{border_color};">
                        <div class="quiz-question-num">{icon} Question {i + 1}</div>
                        <div class="quiz-question-text">{q['question']}</div>
                        <div style="font-size:0.88rem; color:var(--text-secondary);">
                            Your answer: <b>{selected}</b><br/>
                            Correct answer: <b style="color:var(--success);">{correct_option}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Score display
                pct = int((score / total) * 100)
                ring_class = "score-great" if pct >= 70 else ("score-ok" if pct >= 40 else "score-low")

                st.markdown(f"""
                <div style="text-align:center; margin:32px 0;">
                    <div class="score-ring {ring_class}" style="--pct:{pct}%;">
                        <div class="score-inner">{pct}%</div>
                    </div>
                    <div style="font-size:1.3rem; font-weight:700; color:var(--text-primary);">
                        {score} / {total} Correct
                    </div>
                    <div style="font-size:0.88rem; color:var(--text-muted); margin-top:4px;">
                        {'🎉 Excellent work!' if pct >= 80 else '👍 Good effort!' if pct >= 50 else '📖 Keep studying!'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🔄 Retake Quiz"):
                    st.session_state["quiz_submitted"] = False
                    st.session_state["quiz_answers"] = {}
                    st.rerun()
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">❓</div>
                <div class="empty-state-title">No quiz generated yet</div>
                <div class="empty-state-desc">Configure difficulty and scope above, then click "Build Quiz".</div>
            </div>
            """, unsafe_allow_html=True)