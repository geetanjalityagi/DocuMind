import streamlit as st
import requests
import uuid
import time

# ─── Configuration ────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DocuMind — AI Document Intelligence & Adaptive Learning",
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

/* ── Segmented Radio Navigation ─────────────────────────────────────────── */
div[data-testid="stRadio"] > div {
    gap: 8px;
    background: var(--bg-secondary) !important;
    padding: 6px 10px;
    border-radius: 12px;
    border: 1px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
}
div[data-testid="stRadio"] label {
    background: transparent !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    transition: all 0.2s ease !important;
    cursor: pointer;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(99, 102, 241, 0.12) !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
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

/* Secondary Button Outline */
.stButton > button[kind="secondary"] {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    background: rgba(99, 102, 241, 0.1) !important;
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
    padding: 24px 28px;
    margin-bottom: 16px;
    transition: border 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    border-color: var(--border-hover);
    box-shadow: 0 8px 30px rgba(99,102,241,0.10);
}

/* ── Action Selection Cards ──────────────────────────────────────────────── */
.action-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 26px 22px 20px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}
.action-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    opacity: 0;
    transition: opacity 0.3s ease;
}
.action-card:hover {
    border-color: var(--accent-light);
    transform: translateY(-4px);
    box-shadow: 0 14px 34px rgba(99, 102, 241, 0.22);
}
.action-card:hover::before {
    opacity: 1;
}
.action-card-icon {
    font-size: 2.8rem;
    margin-bottom: 10px;
}
.action-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.action-card-desc {
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ── Adaptive Engine & Badges ────────────────────────────────────────────── */
.badge-mastered {
    background: rgba(52, 211, 153, 0.15);
    color: #34D399;
    border: 1px solid rgba(52, 211, 153, 0.3);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
}
.badge-developing {
    background: rgba(99, 102, 241, 0.15);
    color: #818CF8;
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
}
.badge-struggling {
    background: rgba(248, 113, 113, 0.15);
    color: #F87171;
    border: 1px solid rgba(248, 113, 113, 0.3);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
}
.rec-box {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.12));
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
}
.path-node {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
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
    padding: 32px 20px 20px;
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
    font-size: 1.02rem;
    color: var(--text-muted);
    font-weight: 400;
    line-height: 1.6;
}

/* ── Empty State ─────────────────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
}
.empty-state-icon {
    font-size: 3.5rem;
    margin-bottom: 14px;
    opacity: 0.6;
}
.empty-state-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.empty-state-desc {
    font-size: 0.9rem;
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
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in {
    animation: fadeInUp 0.4s ease-out forwards;
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
    "documents": {},          # {doc_id: {filename, title, chunks_size, file_size, page_count}}
    "active_doc_id": None,
    "selected_tab": None,     # None = show action chooser grid; "chat", "notes", etc.
    "chat_history": [],
    "flashcards": [],
    "flashcard_idx": 0,
    "show_card_answer": False,
    "notes_content": None,
    "topics_list": None,
    "quiz_questions": None,
    "quiz_submitted": False,
    "quiz_answers": {},
    "quiz_confidences": {},
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ─── Upload Handler ───────────────────────────────────────────────────────────
def handle_document_upload(file):
    with st.spinner("Parsing, chunking & embedding document…"):
        files = {"file": (file.name, file.getvalue(), "application/pdf")}
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
                    "page_count": data.get("page_count", 0),
                }
                st.session_state["active_doc_id"] = doc_id
                st.session_state["selected_tab"] = None  # Show action chooser
                st.session_state["chat_history"] = []
                st.session_state["notes_content"] = None
                st.session_state["topics_list"] = None
                st.session_state["quiz_questions"] = None
                st.session_state["flashcards"] = []
                return True, data
            else:
                return False, "Upload failed. Check backend logs."
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to backend. Is the server running?"
        except Exception as e:
            return False, f"Error: {e}"


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0px 0 5px;">
        <div style="font-size:3.0rem;">🧠</div>
        <div style="font-size:2.4rem; font-weight:800;
            background: linear-gradient(135deg, #6366F1, #A855F7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;">DocuMind</div>
        <div style="font-size:0.80rem; color:#64748B; margin-top:2px;">
            AI Document Intelligence & Adaptive Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Upload Section ───────────────────────────────────────────────────────
    st.markdown("## 📄 Upload PDF")
    sidebar_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        key="sidebar_pdf_uploader",
        label_visibility="collapsed",
    )

    if sidebar_file is not None:
        if st.button("⚡ Ingest Document", type="primary", use_container_width=True, key="btn_side_ingest"):
            ok, result = handle_document_upload(sidebar_file)
            if ok:
                st.markdown(f"""
                <div class="upload-badge">
                    <div class="upload-badge-text">
                        ✅ {result['filename']} processed — {result.get('chunks_size',0)} chunks
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()
            else:
                st.error(result)

    # ── Document Selector ────────────────────────────────────────────────────
    if st.session_state["documents"]:
        st.divider()
        st.markdown("### 📚 Active Document")
        doc_options = list(st.session_state["documents"].keys())
        cur_active = st.session_state["active_doc_id"]
        cur_idx = doc_options.index(cur_active) if cur_active in doc_options else 0

        selected_id = st.selectbox(
            "Select Document",
            options=doc_options,
            format_func=lambda x: st.session_state["documents"][x]["filename"],
            index=cur_idx,
            label_visibility="collapsed",
            key="sidebar_doc_select",
        )
        if selected_id != st.session_state["active_doc_id"]:
            st.session_state["active_doc_id"] = selected_id
            st.session_state["selected_tab"] = None
            st.rerun()

        doc_meta = st.session_state["documents"][selected_id]
        size_kb = doc_meta["file_size"] / 1024
        size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb / 1024:.1f} MB"
        st.markdown(f"""
        <div class="doc-info-chip">
            📄 <b>{doc_meta['filename']}</b><br/>
            🧩 {doc_meta['chunks_size']} chunks &nbsp;·&nbsp; 📦 {size_str}
        </div>
        """, unsafe_allow_html=True)

        if st.button("➕ Ingest Another PDF", use_container_width=True, key="btn_new_doc"):
            st.session_state["active_doc_id"] = None
            st.session_state["selected_tab"] = None
            st.rerun()

    # ── Session Footer ───────────────────────────────────────────────────────
    st.divider()
    st.caption(f"🔑 Session `{st.session_state['session_id'][:8]}…`")


# ─── Feature Renderers ────────────────────────────────────────────────────────

def render_chat(active_doc_id):
    st.markdown("""
    <div class="glass-card" style="margin-bottom:20px;">
        <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
            💬 Ask Anything About Your Document
        </div>
        <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
            Powered by RAG — answers are synthesized using relevant document chunks.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Display chat history
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


def render_notes(active_doc_id, active_doc_name):
    st.markdown("""
    <div class="glass-card" style="margin-bottom:20px;">
        <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
            📝 AI-Generated Study Notes
        </div>
        <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
            Synthesize key definitions, core concepts, and comprehensive summaries from your document.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Generate Study Notes", type="primary", use_container_width=False):
        with st.spinner("Summarizing document content — this may take a moment…"):
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
            <div class="empty-state-desc">Click "Generate Study Notes" above to create structured revision notes.</div>
        </div>
        """, unsafe_allow_html=True)


def render_topics(active_doc_id):
    st.markdown("""
    <div class="glass-card" style="margin-bottom:20px;">
        <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
            🗂️ Key Topics in Your Document
        </div>
        <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
            AI identifies and organizes the main topics and conceptual themes covered.
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
            <div class="empty-state-desc">Click "Extract Topics" above to discover the key themes.</div>
        </div>
        """, unsafe_allow_html=True)


def render_flashcards(active_doc_id):
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

    fc1, fc2, fc3 = st.columns([2, 2, 1])
    with fc1:
        gen_mode = st.selectbox("Scope", ["full_document", "topic"], key="fc_mode")
    with fc2:
        topic_input = st.text_input(
            "Topic (if scope = topic)", value="", key="fc_topic",
            placeholder="e.g. Relational Schema"
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

    cards = st.session_state["flashcards"]
    if cards:
        idx = st.session_state["flashcard_idx"]
        card = cards[idx]
        progress_pct = ((idx + 1) / len(cards)) * 100

        st.markdown(f"""
        <div class="card-counter">{idx + 1} / {len(cards)}</div>
        <div class="card-progress">
            <div class="card-progress-bar" style="width:{progress_pct}%;"></div>
        </div>
        """, unsafe_allow_html=True)

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
            <div class="empty-state-desc">Configure scope above and click "Generate Deck".</div>
        </div>
        """, unsafe_allow_html=True)


def render_quiz(active_doc_id):
    st.markdown("""
    <div class="glass-card" style="margin-bottom:20px;">
        <div style="font-size:1.15rem; font-weight:700; color:var(--text-primary);">
            ❓ Multiple Choice Assessment
        </div>
        <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
            Auto-generated quizzes with confidence tracking and instant Bayesian calibration.
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                    st.session_state["quiz_confidences"] = {}
                    st.rerun()
                else:
                    st.error("Failed to generate quiz.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend.")
            except Exception as e:
                st.error(f"Error: {e}")

    questions = st.session_state["quiz_questions"]
    if questions:
        if not st.session_state["quiz_submitted"]:
            with st.form("quiz_form"):
                user_answers = {}
                user_confidences = {}
                for i, q in enumerate(questions):
                    st.markdown(f"""
                    <div class="quiz-question-card">
                        <div class="quiz-question-num">Question {i + 1} of {len(questions)} &nbsp;·&nbsp; Topic: {q.get('topic', 'General')}</div>
                        <div class="quiz-question-text">{q['question']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    user_answers[i] = st.radio(
                        f"Select answer for Q{i + 1}",
                        options=q["options"],
                        key=f"q_{i}",
                        label_visibility="collapsed",
                    )
                    user_confidences[i] = st.slider(
                        f"Confidence in your answer (Q{i + 1})",
                        min_value=10,
                        max_value=100,
                        value=70,
                        step=10,
                        key=f"conf_{i}",
                        help="Confidence rating helps the Adaptive Engine calibrate your metacognition and detect misconceptions.",
                    )

                submitted = st.form_submit_button("📊 Submit Quiz to Adaptive Engine", use_container_width=True)
                if submitted:
                    st.session_state["quiz_answers"] = user_answers
                    st.session_state["quiz_confidences"] = user_confidences
                    st.session_state["quiz_submitted"] = True

                    # Package attempts for the adaptive learning engine
                    attempts = []
                    for i, q in enumerate(questions):
                        selected = user_answers.get(i, "")
                        correct_letter = q["correct_answer"]
                        correct_option = (
                            q["options"]["ABCD".index(correct_letter)]
                            if len(correct_letter) == 1 and correct_letter in "ABCD"
                            else correct_letter
                        )
                        is_correct = selected == correct_option
                        attempts.append({
                            "topic": q.get("topic", "General"),
                            "difficulty": difficulty,
                            "is_correct": is_correct,
                            "confidence": float(user_confidences.get(i, 70)),
                            "question_text": q.get("question"),
                            "user_answer": selected,
                            "correct_answer": correct_option,
                        })

                    # Send to backend
                    try:
                        requests.post(
                            f"{BACKEND_URL}/learning/submit-quiz",
                            json={
                                "session_id": st.session_state["session_id"],
                                "document_id": active_doc_id,
                                "attempts": attempts,
                            },
                            timeout=10,
                        )
                    except Exception:
                        pass

                    st.rerun()
        else:
            user_answers = st.session_state["quiz_answers"]
            user_confidences = st.session_state.get("quiz_confidences", {})
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
                conf_val = user_confidences.get(i, 70)

                # Calibration check for this question
                calib_badge = ""
                if not is_correct and conf_val >= 70:
                    calib_badge = '<span style="color:#F87171; font-size:0.8rem; font-weight:700;">⚠️ Potential Misconception (High Confidence on Incorrect Answer)</span>'
                elif is_correct and conf_val <= 40:
                    calib_badge = '<span style="color:#818CF8; font-size:0.8rem; font-weight:700;">💡 Tentative Knowledge (Correct despite Low Confidence)</span>'

                st.markdown(f"""
                <div class="quiz-question-card" style="border-color:{border_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div class="quiz-question-num">{icon} Question {i + 1} &nbsp;·&nbsp; {q.get('topic', 'General')}</div>
                        {calib_badge}
                    </div>
                    <div class="quiz-question-text">{q['question']}</div>
                    <div style="font-size:0.88rem; color:var(--text-secondary);">
                        Your answer: <b>{selected}</b> (Confidence: {conf_val}%)<br/>
                        Correct answer: <b style="color:var(--success);">{correct_option}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

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
                    &nbsp;·&nbsp; <i>Learner profile & BKT knowledge states updated!</i>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_retake, col_dash = st.columns(2)
            with col_retake:
                if st.button("🔄 Retake Quiz", use_container_width=True):
                    st.session_state["quiz_submitted"] = False
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_confidences"] = {}
                    st.rerun()
            with col_dash:
                if st.button("🎯 Open Adaptive Learning Hub", type="primary", use_container_width=True):
                    st.session_state["selected_tab"] = "adaptive"
                    st.rerun()
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">❓</div>
            <div class="empty-state-title">No quiz generated yet</div>
            <div class="empty-state-desc">Configure difficulty and scope above, then click "Build Quiz".</div>
        </div>
        """, unsafe_allow_html=True)


def render_adaptive_learning(active_doc_id):
    st.markdown("""
    <div class="glass-card" style="margin-bottom:20px;">
        <div style="font-size:1.25rem; font-weight:800; color:var(--text-primary);">
            🎯 Adaptive Learning Engine & Knowledge Tracer
        </div>
        <div style="font-size:0.86rem; color:var(--text-muted); margin-top:4px;">
            Powered by Bayesian Knowledge Tracing (BKT), multi-difficulty mastery weighting, spaced repetition (SM-2), and cognitive error-pattern diagnostics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        res = requests.get(f"{BACKEND_URL}/learning/profile/{st.session_state['session_id']}/{active_doc_id}")
        if res.status_code != 200:
            st.error("Could not fetch learner profile.")
            return
        profile = res.json()
    except Exception as e:
        st.error(f"Cannot connect to backend: {e}")
        return

    # Check if learner has attempts
    total_q = profile.get("total_questions_attempted", 0)
    if total_q == 0:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📊</div>
            <div class="empty-state-title">No Knowledge Data Yet</div>
            <div class="empty-state-desc" style="max-width: 540px; margin: 0 auto 20px;">
                Complete a quiz or answer questions to calibrate your knowledge profile. DocuMind will model your topic mastery, track knowledge via BKT, detect blind spots (like Student A vs Student B patterns), and schedule spaced revisions.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Start a Diagnostic Quiz", type="primary", use_container_width=True):
            st.session_state["selected_tab"] = "quiz"
            st.rerun()
        return

    # 1. Top Metrics Bar
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{profile.get('overall_mastery', 0):.0f}%</div>
            <div class="stat-label">Weighted Mastery</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        bkt_val = profile.get('overall_bkt', 0.2)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{bkt_val * 100:.0f}%</div>
            <div class="stat-label">BKT Knowledge State P(L)</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{profile.get('overall_accuracy', 0):.0f}%</div>
            <div class="stat-label">Accuracy ({total_q} questions)</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        due_count = len(profile.get("due_reviews", []))
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color: {'#FBBF24' if due_count > 0 else '#34D399'};">{due_count}</div>
            <div class="stat-label">Spaced Reviews Due</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Next Best Learning Action (Recommendation with Transparent Explanation)
    rec = profile.get("primary_recommendation")
    if rec:
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        urgency_color = "#F87171" if rec.get("urgency") in ("critical_review", "foundation_repair") else "#818CF8"
        st.markdown(f"""
        <div class="rec-box animate-in">
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.12em; color:{urgency_color}; margin-bottom:6px;">
                ⚡ Recommended Next Action ({rec.get('urgency').replace('_', ' ').title()})
            </div>
            <div style="font-size:1.35rem; font-weight:800; color:#fff; margin-bottom:8px;">
                {rec.get('recommended_activity').replace('_', ' ').title()} on <u>{rec.get('topic')}</u> ({rec.get('recommended_difficulty').upper()} Difficulty)
            </div>
            <div style="background: rgba(11, 15, 26, 0.6); padding: 14px 16px; border-radius: 10px; border-left: 3px solid {urgency_color}; margin-bottom: 12px;">
                <div style="font-size:0.85rem; color:#94A3B8; font-weight:600; margin-bottom:2px;">Pedagogical Reason (The "Why"):</div>
                <div style="font-size:0.95rem; color:#F1F5F9; line-height:1.5;">{rec.get('reasoning')}</div>
            </div>
            <div style="font-size:0.85rem; color:#A855F7;">
                🎯 <b>Pedagogical Goal:</b> {rec.get('pedagogical_goal')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"🚀 Launch Recommended Action: {rec.get('recommended_activity').replace('_', ' ').title()}", type="primary", use_container_width=True):
            act = rec.get("recommended_activity")
            if act in ("quiz_practice", "mastery_challenge"):
                st.session_state["selected_tab"] = "quiz"
                st.session_state["qz_diff"] = rec.get("recommended_difficulty", "medium")
                st.session_state["qz_mode"] = "topic"
                st.session_state["qz_topic"] = rec.get("topic")
            elif act == "flashcard_revision":
                st.session_state["selected_tab"] = "cards"
                st.session_state["fc_mode"] = "topic"
                st.session_state["fc_topic"] = rec.get("topic")
            elif act == "notes_review":
                st.session_state["selected_tab"] = "notes"
            st.rerun()

    # 3. Weakness & Cognitive Error Patterns Section
    weaknesses = profile.get("weaknesses", [])
    if weaknesses:
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("### 🔍 Cognitive Error Patterns & Diagnostic Alerts")
        for w in weaknesses:
            p_type = w.get("pattern_type")
            title = p_type.replace("_", " ").title()
            border = "rgba(248, 113, 113, 0.4)" if w.get("severity") == "high" else "rgba(251, 191, 36, 0.4)"
            st.markdown(f"""
            <div class="glass-card animate-in" style="border-left: 4px solid {border}; margin-bottom: 12px; padding: 16px 20px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; color:var(--text-primary); font-size:1.0rem;">
                        ⚠️ {title} — <span style="color:var(--accent-light);">{w.get('topic')}</span>
                    </span>
                    <span style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:{'#F87171' if w.get('severity')=='high' else '#FBBF24'};">
                        {w.get('severity')} priority
                    </span>
                </div>
                <div style="font-size:0.88rem; color:var(--text-secondary); margin: 6px 0;">
                    {w.get('summary')}
                </div>
                <div style="font-size:0.84rem; color:#34D399; font-weight:500;">
                    💡 <b>Actionable Tip:</b> {w.get('actionable_tip')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 4. Detailed Topic Mastery Profiles
    topics = profile.get("topic_profiles", {})
    if topics:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📊 Topic-by-Topic Learner Modeling")
        for t_name, t_data in topics.items():
            status = t_data.get("learning_status", "developing")
            badge_class = f"badge-{status}" if status in ("mastered", "struggling", "developing") else "badge-developing"
            mastery = t_data.get("mastery_score", 0.0)
            bkt = t_data.get("bkt_p_known", 0.20) * 100.0

            st.markdown(f"""
            <div class="glass-card animate-in" style="margin-bottom:14px; padding: 18px 22px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="font-size:1.1rem; font-weight:700; color:var(--text-primary);">{t_name}</span>
                        <span class="{badge_class}" style="margin-left:10px;">{status}</span>
                        <span style="margin-left:8px; font-size:0.78rem; color:var(--text-muted);">
                            Calibration: <b>{t_data.get('calibration_status', 'uncalibrated').replace('_', ' ').title()}</b>
                        </span>
                    </div>
                    <div style="font-size:1.15rem; font-weight:800; color:var(--accent-light);">
                        {mastery:.0f}% Mastery
                    </div>
                </div>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; font-size:0.84rem; color:var(--text-secondary);">
                    <div>🧠 <b>BKT Probability:</b> {bkt:.1f}%</div>
                    <div>🟢 <b>Easy:</b> {t_data.get('easy_accuracy', 0):.0f}% ({t_data.get('easy_correct', 0)}/{t_data.get('easy_attempts', 0)})</div>
                    <div>🟡 <b>Medium:</b> {t_data.get('medium_accuracy', 0):.0f}% ({t_data.get('medium_correct', 0)}/{t_data.get('medium_attempts', 0)})</div>
                    <div>🔴 <b>Hard:</b> {t_data.get('hard_accuracy', 0):.0f}% ({t_data.get('hard_correct', 0)}/{t_data.get('hard_attempts', 0)})</div>
                </div>
                <div style="margin-top:8px; font-size:0.78rem; color:var(--text-muted); display:flex; justify-content:space-between;">
                    <span>🔥 Streak: <b>{t_data.get('consecutive_correct', 0)}</b> correct</span>
                    <span>⏳ Next Spaced Review: <b>{t_data.get('next_review', 'N/A')[:10] if t_data.get('next_review') else 'Not scheduled'}</b> (Interval: {t_data.get('interval_days', 1)}d)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 5. Adaptive Learning Path (Prerequisites & Milestone RoadMap)
    try:
        path_res = requests.get(f"{BACKEND_URL}/learning/path/{st.session_state['session_id']}/{active_doc_id}")
        if path_res.status_code == 200:
            path_data = path_res.json()
            nodes = path_data.get("nodes", [])
            if nodes:
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                st.markdown("### 🗺️ Adaptive Learning Path & Prerequisites")
                for node in nodes:
                    n_status = node.get("status")
                    icon = "🔒" if n_status == "locked" else ("✅" if n_status == "mastered" else ("⏳" if n_status == "review_due" else "🎯"))
                    border_color = "var(--border)" if n_status == "locked" else ("var(--success)" if n_status == "mastered" else "var(--accent)")
                    st.markdown(f"""
                    <div class="path-node animate-in" style="border-left: 4px solid {border_color};">
                        <div>
                            <span style="font-size:1.05rem; font-weight:700; color:var(--text-primary);">
                                {icon} Step {node.get('order_index')}: {node.get('topic')}
                            </span>
                            <div style="font-size:0.82rem; color:var(--text-muted); margin-top:2px;">
                                {node.get('recommended_next_step')}
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:0.95rem; font-weight:700; color:var(--accent-light);">
                                {node.get('mastery_score', 0):.0f}%
                            </span>
                            <div style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted);">
                                {n_status.replace('_', ' ')}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    except Exception:
        pass


# ─── Main Area Controller ────────────────────────────────────────────────────

# ═════════════════════════════════════════════════════════════════════════════
# 1. NO DOCUMENT UPLOADED YET — Show Clean Landing & Upload Screen
# ═════════════════════════════════════════════════════════════════════════════
if not st.session_state["active_doc_id"]:
    st.markdown("""
    <div class="hero-header animate-in">
        <div style="font-size: 3.5rem; margin-bottom: 6px;">🧠</div>
        <div class="hero-title">DocuMind Intelligence</div>
        <div class="hero-subtitle" style="max-width: 620px; margin: 0 auto;">
            Upload any PDF to unlock AI-powered conversational Q&A, comprehensive study notes, topic extraction, flashcards, quizzes, and the <b>Adaptive Learning Engine</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean, focused center upload area
    up_c1, up_c2, up_c3 = st.columns([1, 2.4, 1])
    with up_c2:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding: 28px 24px 20px; border: 2px dashed rgba(99, 102, 241, 0.45); margin-top: 12px;">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">📄</div>
            <div style="font-weight: 700; font-size: 1.15rem; color: var(--text-primary); margin-bottom: 4px;">
                Select or Drop your PDF
            </div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
                Supported format: PDF documents up to 50MB
            </div>
        </div>
        """, unsafe_allow_html=True)

        center_file = st.file_uploader(
            "Upload PDF here",
            type=["pdf"],
            key="center_pdf_uploader",
            label_visibility="collapsed"
        )

        if center_file is not None:
            if st.button("⚡ Ingest & Analyze Document", type="primary", use_container_width=True, key="btn_center_ingest"):
                ok, result = handle_document_upload(center_file)
                if ok:
                    st.rerun()
                else:
                    st.error(result)

        # 3-step simple guide
        st.markdown("""
        <div style="display: flex; justify-content: space-around; align-items: center; margin-top: 40px; padding: 18px 20px; background: rgba(17, 24, 39, 0.45); border-radius: 14px; border: 1px solid var(--border);">
            <div style="text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent-light); letter-spacing: 0.1em; text-transform: uppercase;">Step 1</div>
                <div style="font-size: 0.90rem; font-weight: 600; color: var(--text-primary); margin-top: 2px;">Upload PDF</div>
            </div>
            <div style="color: var(--text-muted); font-size: 1.1rem;">→</div>
            <div style="text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent-light); letter-spacing: 0.1em; text-transform: uppercase;">Step 2</div>
                <div style="font-size: 0.90rem; font-weight: 600; color: var(--text-primary); margin-top: 2px;">Choose Mode</div>
            </div>
            <div style="color: var(--text-muted); font-size: 1.1rem;">→</div>
            <div style="text-align: center;">
                <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent-light); letter-spacing: 0.1em; text-transform: uppercase;">Step 3</div>
                <div style="font-size: 0.90rem; font-weight: 600; color: var(--text-primary); margin-top: 2px;">Adaptive Study</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# 2. DOCUMENT IS UPLOADED — Show Action Selector or Selected Feature
# ═════════════════════════════════════════════════════════════════════════════
else:
    active_doc_id = st.session_state["active_doc_id"]
    active_doc = st.session_state["documents"][active_doc_id]
    active_doc_name = active_doc["filename"]
    size_kb = active_doc.get("file_size", 0) / 1024
    size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb / 1024:.1f} MB"
    chunks_count = active_doc.get("chunks_size", 0)

    # ── CASE 2A: Action Chooser Grid (User hasn't picked a tool yet) ───────────
    if st.session_state["selected_tab"] is None:
        # Document Header Card
        st.markdown(f"""
        <div class="glass-card animate-in" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:24px;">
            <div>
                <div style="font-size:0.75rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--accent-light); margin-bottom:4px;">
                    Active Document
                </div>
                <div style="font-size:1.5rem; font-weight:800; color:var(--text-primary);">
                    📄 {active_doc_name}
                </div>
                <div style="font-size:0.84rem; color:var(--text-muted); margin-top:4px;">
                    🧩 <b>{chunks_count}</b> chunks embedded &nbsp;·&nbsp; 📦 <b>{size_str}</b> &nbsp;·&nbsp; ✅ Ready for AI & Adaptive Features
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; margin: 18px 0 26px;">
            <div style="font-size: 2.1rem; font-weight: 800;
                background: linear-gradient(135deg, #6366F1, #A855F7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent; margin-bottom: 6px;">
                What would you like to do?
            </div>
            <div style="color: var(--text-muted); font-size: 0.96rem;">
                Select any feature below to start exploring, assessing, and adaptively mastering this document:
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Row 1: 3 Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="action-card animate-in">
                <div class="action-card-icon">🎯</div>
                <div class="action-card-title">Adaptive Engine</div>
                <div class="action-card-desc">
                    Bayesian Knowledge Tracing (BKT), error-pattern diagnostics (Student A vs B), spaced repetition, and personalized learning paths.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🎯 Open Adaptive Engine", use_container_width=True, type="primary", key="btn_act_adaptive"):
                st.session_state["selected_tab"] = "adaptive"
                st.rerun()

        with col2:
            st.markdown("""
            <div class="action-card animate-in" style="animation-delay:0.05s;">
                <div class="action-card-icon">❓</div>
                <div class="action-card-title">Quiz Assessment</div>
                <div class="action-card-desc">
                    Take multiple-choice tests with confidence tracking and instant auto-grading that updates your knowledge profile.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("❓ Take Quiz", use_container_width=True, type="primary", key="btn_act_quiz"):
                st.session_state["selected_tab"] = "quiz"
                st.rerun()

        with col3:
            st.markdown("""
            <div class="action-card animate-in" style="animation-delay:0.1s;">
                <div class="action-card-icon">💬</div>
                <div class="action-card-title">Chat Q&A</div>
                <div class="action-card-desc">
                    Ask questions and get instant, context-aware answers retrieved directly from document chunks.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("💬 Start Chatting", use_container_width=True, type="primary", key="btn_act_chat"):
                st.session_state["selected_tab"] = "chat"
                st.rerun()

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Row 2: 3 Cards
        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown("""
            <div class="action-card animate-in" style="animation-delay:0.15s;">
                <div class="action-card-icon">📝</div>
                <div class="action-card-title">Study Notes</div>
                <div class="action-card-desc">
                    Synthesize key definitions, core concepts, and comprehensive revision notes from the document.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📝 Generate Notes", use_container_width=True, type="primary", key="btn_act_notes"):
                st.session_state["selected_tab"] = "notes"
                st.rerun()

        with col5:
            st.markdown("""
            <div class="action-card animate-in" style="animation-delay:0.2s;">
                <div class="action-card-icon">🃏</div>
                <div class="action-card-title">Flashcards</div>
                <div class="action-card-desc">
                    Reinforce memory retention with question-answer flip cards tailored to the entire document or a topic.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🃏 Practice Flashcards", use_container_width=True, type="primary", key="btn_act_cards"):
                st.session_state["selected_tab"] = "cards"
                st.rerun()

        with col6:
            st.markdown("""
            <div class="action-card animate-in" style="animation-delay:0.25s;">
                <div class="action-card-icon">🗂️</div>
                <div class="action-card-title">Key Topics</div>
                <div class="action-card-desc">
                    Discover high-level themes, main subjects, and conceptual structure identified by AI.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗂️ Extract Topics", use_container_width=True, type="primary", key="btn_act_topics"):
                st.session_state["selected_tab"] = "topics"
                st.rerun()

    # ── CASE 2B: Specific Feature is Active (User chose a tool) ───────────────
    else:
        action_map = {
            "adaptive": "🎯 Adaptive Engine",
            "quiz": "❓ Quiz",
            "chat": "💬 Chat Q&A",
            "notes": "📝 Study Notes",
            "cards": "🃏 Flashcards",
            "topics": "🗂️ Topics",
        }

        # Top Bar: Document Chip + Back Button + Quick Switch Tabs
        bar_col1, bar_col2 = st.columns([1.1, 3.9])
        with bar_col1:
            if st.button("⬅ All Actions", use_container_width=True, key="btn_back_to_menu"):
                st.session_state["selected_tab"] = None
                st.rerun()

        with bar_col2:
            cur_tab = st.session_state["selected_tab"]
            cur_idx = list(action_map.keys()).index(cur_tab) if cur_tab in action_map else 0
            picked_action = st.radio(
                "Feature Navigation",
                options=list(action_map.values()),
                index=cur_idx,
                horizontal=True,
                label_visibility="collapsed",
                key="top_feature_nav_radio"
            )
            new_tab = [k for k, v in action_map.items() if v == picked_action][0]
            if new_tab != st.session_state["selected_tab"]:
                st.session_state["selected_tab"] = new_tab
                st.rerun()

        st.caption(f"📄 Active: **{active_doc_name}** ({chunks_count} chunks)")
        st.divider()

        # Render the selected feature
        if st.session_state["selected_tab"] == "adaptive":
            render_adaptive_learning(active_doc_id)
        elif st.session_state["selected_tab"] == "quiz":
            render_quiz(active_doc_id)
        elif st.session_state["selected_tab"] == "chat":
            render_chat(active_doc_id)
        elif st.session_state["selected_tab"] == "notes":
            render_notes(active_doc_id, active_doc_name)
        elif st.session_state["selected_tab"] == "topics":
            render_topics(active_doc_id)
        elif st.session_state["selected_tab"] == "cards":
            render_flashcards(active_doc_id)
