import streamlit as st
import requests
import uuid

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DocuMind — Document Intelligence & Adaptive Learning",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Google Font ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Black Palette Tokens ────────────────────────────────────────────────── */
:root {
    --bg-page:       #000000;
    --bg-sidebar:    #09090B;
    --bg-card:       #121214;
    --bg-card-hover: #18181B;
    --bg-input:      #0E0E10;
    --border-subtle: #222226;
    --border-hover:  #383840;
    --border-active: #52525B;
    --text-primary:  #FFFFFF;
    --text-secondary:#A1A1AA;
    --text-muted:    #71717A;
    --accent:        #FFFFFF;
    --accent-bg:     #1E1E24;
    --success:       #10B981;
    --warning:       #F59E0B;
    --danger:        #EF4444;
}

/* ── Global Resets ───────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], .main,
[data-testid="stApp"] {
    background-color: var(--bg-page) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
    z-index: 100 !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
}
section[data-testid="stSidebar"] hr {
    margin: 8px 0 !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Sidebar Navigation Tabs ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] div.stButton > button {
    font-size: 0.83rem !important;
    padding: 6px 10px !important;
    min-height: 34px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    margin-bottom: 6px !important;
    line-height: 1.25 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.15s ease !important;
}
/* Active Tab: Refined dark charcoal with subtle border & accent line (no glaring white!) */
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: #1C1C22 !important;
    color: #FFFFFF !important;
    border: 1px solid #383842 !important;
    border-left: 4px solid #818CF8 !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4) !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
    background: #24242C !important;
    border-color: #52525E !important;
    color: #FFFFFF !important;
}
/* Inactive Tabs: Clean transparent/dark with subtle hover */
section[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #A1A1AA !important;
    border: 1px solid transparent !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
    background-color: #141418 !important;
    border-color: #27272A !important;
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] div[data-testid="column"] div.stButton > button {
    font-size: 0.78rem !important;
    padding: 5px 8px !important;
    min-height: 32px !important;
    text-align: center !important;
    justify-content: center !important;
}

/* ── Buttons (Clean Minimalist Monochrome) ──────────────────────────────── */
.stButton > button {
    background-color: #18181B !important;
    color: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    font-weight: 500 !important;
    font-size: 0.90rem !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background-color: #27272A !important;
    border-color: var(--border-hover) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Primary Button (White on Black) */
.stButton > button[kind="primary"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #FFFFFF !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #E4E4E7 !important;
    border-color: #E4E4E7 !important;
    color: #000000 !important;
}

/* ── Input Fields & Selects ──────────────────────────────────────────────── */
.stTextInput > div > div,
.stNumberInput > div > div,
.stSelectbox > div > div,
.stFileUploader > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stSelectbox > div > div:focus-within {
    border-color: var(--border-active) !important;
}
input, textarea {
    color: var(--text-primary) !important;
}
label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
}

/* ── Chat Messages (Clean ChatGPT/Claude Dark Style) ───────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    border-radius: 0px !important;
    padding: 20px 12px !important;
    margin-bottom: 0px !important;
}
[data-testid="stChatMessage"]:last-child {
    border-bottom: none !important;
}

/* ── Content Container (Chat, Quiz, Flashcards, Adaptive Learning, Topics, Study Notes) ── */
.main .block-container,
[data-testid="stMainBlockContainer"] {
    max-width: 1080px !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 1.8rem !important;
    padding-bottom: 6rem !important;
    box-sizing: border-box !important;
}

/* ── Bottom Question Bar ─────────────────────────────────────────────────── */
[data-testid="stBottom"],
div:has(> [data-testid="stChatInput"]) {
    background-color: #000000 !important;
}

[data-testid="stBottom"] {
    background: #000000 !important;
    border-top: 1px solid #1C1C22 !important;
    padding-top: 8px !important;
    padding-bottom: 12px !important;
    z-index: 90 !important;
}

[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"] {
    max-width: 1080px !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    box-sizing: border-box !important;
}

[data-testid="stChatInput"] {
    max-width: 1080px !important;
    width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    background-color: #0E0E12 !important;
    border: 1px solid #27272A !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #52525B !important;
    box-shadow: 0 0 0 1px #52525B, 0 6px 24px rgba(0, 0, 0, 0.8) !important;
}

[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
    background: transparent !important;
    font-size: 0.95rem !important;
    font-family: inherit !important;
    padding: 12px 14px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #71717A !important;
}

[data-testid="stChatInput"] button {
    background: transparent !important;
    border: none !important;
    color: #A1A1AA !important;
    padding-right: 12px !important;
}

[data-testid="stChatInput"] button:hover {
    color: #FFFFFF !important;
}

footer {
    display: none !important;
}

/* ── Cards & Surfaces ────────────────────────────────────────────────────── */
.black-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s ease;
}
.black-card:hover {
    border-color: var(--border-hover);
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 16px 18px;
    text-align: center;
}
.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #FFFFFF;
}
.stat-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 4px;
}

/* ── Status Badges ───────────────────────────────────────────────────────── */
.badge {
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    display: inline-block;
}
.badge-mastered {
    background: rgba(16, 185, 129, 0.12);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.badge-developing {
    background: rgba(255, 255, 255, 0.08);
    color: #E4E4E7;
    border: 1px solid var(--border-subtle);
}
.badge-struggling {
    background: rgba(239, 68, 68, 0.12);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}
.badge-review {
    background: rgba(245, 158, 11, 0.12);
    color: #F59E0B;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

/* ── Flashcard ───────────────────────────────────────────────────────────── */
.flashcard-face {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 36px 32px;
    text-align: center;
    width: 100%;
    max-width: 650px;
    margin: 0 auto;
    transition: border-color 0.2s ease;
}
.flashcard-face:hover {
    border-color: var(--border-hover);
}
.flashcard-label {
    font-size: 0.70rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 12px;
}
.flashcard-text {
    font-size: 1.20rem;
    font-weight: 500;
    color: #FFFFFF;
    line-height: 1.6;
}

/* ── Quiz Question Card ──────────────────────────────────────────────────── */
.quiz-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

/* ── Suggested Prompts Chips ─────────────────────────────────────────────── */
.chip-btn {
    background: #141417;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 12px 16px;
    color: var(--text-secondary);
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.15s ease;
    margin-bottom: 10px;
}
.chip-btn:hover {
    border-color: var(--border-hover);
    color: #FFFFFF;
    background: #1C1C21;
}

/* ── Dividers ────────────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: 16px 0 !important;
}

/* ── Clean Scrollbars ────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-page); }
::-webkit-scrollbar-thumb {
    background: var(--border-subtle);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--border-hover);
}
</style>
""", unsafe_allow_html=True)


defaults = {
    "session_id": str(uuid.uuid4()),
    "documents": {},         
    "active_doc_id": None,
    "active_page": "💬 Chat", 
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


def handle_document_upload(file):
    with st.spinner("Processing document…"):
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
                st.session_state["chat_history"] = []
                st.session_state["notes_content"] = None
                st.session_state["topics_list"] = None
                st.session_state["quiz_questions"] = None
                st.session_state["flashcards"] = []
                return True, data
            else:
                return False, f"Upload failed ({res.status_code})"
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to backend server."
        except Exception as e:
            return False, f"Error: {e}"


def get_api_error(response):
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if isinstance(payload, dict) and payload.get("detail"):
        return str(payload["detail"])

    return response.text.strip() or f"HTTP {response.status_code}"


with st.sidebar:
    st.markdown("""
    <div style="padding: 4px 2px 18px; text-align: center;">
        <div style="font-size: 1.7rem; font-weight: 800; color: #FFFFFF; display: flex; align-items: center; justify-content: center; gap: 7px; letter-spacing: -0.02em; line-height: 1.15;">
            <span style="font-size: 1.5rem; line-height: 1;">🧠</span> <span>DocuMind</span>
        </div>
        <div style="font-size: 0.86rem; color: #A1A1AA; font-weight: 500; margin-top: 3px; text-align: center;">
            AI Document Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="sidebar_file_uploader",
        label_visibility="collapsed",
    )
    if uploaded_pdf is not None:
        if st.button("Upload Document", type="primary", use_container_width=True, key="btn_side_upload"):
            ok, res = handle_document_upload(uploaded_pdf)
            if ok:
                st.rerun()
            else:
                st.error(res)

    st.divider()

    st.markdown("<div style='font-size: 0.92rem; font-weight: 700; letter-spacing: 0.01em; color: #D4D4D8; margin: 2px 0 10px; text-align: center;'>Workspace Navigation</div>", unsafe_allow_html=True)

    nav_tabs = [
        ("💬 Chat", "💬 Chat"),
        ("🎯 Adaptive Engine", "🎯 Adaptive Engine"),
        ("❓ Quiz", "❓ Quiz"),
        ("🃏 Flashcards", "🃏 Flashcards"),
        ("📝 Study Notes", "📝 Study Notes"),
        ("🗂️ Topics", "🗂️ Topics"),
    ]

    for label, page_key in nav_tabs:
        is_active = (st.session_state["active_page"] == page_key)
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_tab_{page_key}", use_container_width=True, type=btn_type):
            if st.session_state["active_page"] != page_key:
                st.session_state["active_page"] = page_key
                st.rerun()

    if st.session_state["documents"]:
        st.divider()
        st.markdown("<div style='font-size: 0.92rem; font-weight: 700; letter-spacing: 0.01em; color: #D4D4D8; margin: 2px 0 10px; text-align: center;'>Active Document</div>", unsafe_allow_html=True)

        doc_options = list(st.session_state["documents"].keys())
        cur_doc = st.session_state["active_doc_id"]
        doc_idx = doc_options.index(cur_doc) if cur_doc in doc_options else 0

        selected_doc = st.selectbox(
            "Select Document",
            options=doc_options,
            format_func=lambda x: st.session_state["documents"][x]["filename"],
            index=doc_idx,
            label_visibility="collapsed",
            key="sidebar_doc_selector",
        )
        if selected_doc != st.session_state["active_doc_id"]:
            st.session_state["active_doc_id"] = selected_doc
            st.rerun()

    st.divider()

    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        if st.button("🗑️ Clear Chat", use_container_width=True, key="btn_clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()
    with col_s2:
        st.markdown(f"<div style='font-size: 0.70rem; color: #52525B; padding-top: 4px; text-align: right;'>Session `{st.session_state['session_id'][:6]}`</div>", unsafe_allow_html=True)


def render_chat_page(active_doc_id):
    active_meta = st.session_state["documents"].get(active_doc_id) if active_doc_id else None
    doc_name = active_meta["filename"] if active_meta else None

    if doc_name:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 16px;">
            <div>
                <span style="font-size: 1.15rem; font-weight: 600; color: #FFFFFF;">Chat</span>
                <span style="font-size: 0.82rem; color: var(--text-muted); margin-left: 10px;">📄 {doc_name}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 16px;">
            <div>
                <span style="font-size: 1.15rem; font-weight: 600; color: #FFFFFF;">Chat</span>
                <span style="font-size: 0.82rem; color: var(--text-muted); margin-left: 10px;">No document active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not st.session_state["chat_history"]:
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px 24px;">
            <div style="font-size: 2.6rem; margin-bottom: 8px;">🧠</div>
            <h2 style="font-size: 1.8rem; font-weight: 700; color: #FFFFFF; margin-bottom: 24px;">
                What would you like to explore?
            </h2>
        </div>
        """, unsafe_allow_html=True)

        if doc_name:
            p1, p2, p3, p4 = st.columns(4, gap="small")
            with p1:
                if st.button("📌 Key findings", use_container_width=True, key="prompt_1"):
                    send_chat_message("Summarize the core findings and main takeaways of this document.", active_doc_id)
            with p2:
                if st.button("🎯 Key concepts", use_container_width=True, key="prompt_2"):
                    send_chat_message("What are the key concepts and definitions explained in this document?", active_doc_id)
            with p3:
                if st.button("🔍 Methodology", use_container_width=True, key="prompt_3"):
                    send_chat_message("Explain the main methodology or framework described in this document.", active_doc_id)
            with p4:
                if st.button("❓ Takeaways", use_container_width=True, key="prompt_4"):
                    send_chat_message("What are the most critical takeaways I should remember?", active_doc_id)

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask a question about the document…")
    if user_prompt:
        if not active_doc_id:
            st.warning("Please upload or select a PDF document in the sidebar first.")
        else:
            send_chat_message(user_prompt, active_doc_id)


def send_chat_message(prompt: str, active_doc_id: str):
    st.session_state["chat_history"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching document context…"):
            payload = {
                "session_id": st.session_state["session_id"],
                "document_id": active_doc_id,
                "question": prompt,
            }
            try:
                res = requests.post(f"{BACKEND_URL}/chats/chat", json=payload, timeout=45)
                if res.status_code == 200:
                    answer = res.json().get("answer", "No response received.")
                    st.markdown(answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                else:
                    st.error("Failed to generate answer. Check backend status.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend server.")
            except Exception as e:
                st.error(f"Error: {e}")
    st.rerun()


def render_adaptive_page(active_doc_id):
    st.markdown("""
    <div style="padding: 10px 0 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 20px;">
        <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">Adaptive Learning Engine</span>
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;">
            Bayesian Knowledge Tracing (BKT), error-pattern diagnostics (Student A vs B), and SM-2 spaced repetition.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not active_doc_id:
        st.info("Select or upload a PDF document in the sidebar to view your adaptive knowledge profile.")
        return

    try:
        res = requests.get(f"{BACKEND_URL}/learning/profile/{st.session_state['session_id']}/{active_doc_id}")
        if res.status_code != 200:
            st.error("Could not fetch learner profile.")
            return
        profile = res.json()
    except Exception as e:
        st.error(f"Cannot connect to backend: {e}")
        return

    total_q = profile.get("total_questions_attempted", 0)
    if total_q == 0:
        st.markdown("""
        <div class="black-card" style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 2.2rem; margin-bottom: 10px;">📊</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">No Learning Data Yet</div>
            <div style="font-size: 0.88rem; color: var(--text-muted); max-width: 480px; margin: 0 auto 20px;">
                Complete a quiz from the sidebar to initialize your Bayesian Knowledge Tracing profile, detect blind spots, and unlock personalized recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Quiz", type="primary"):
            st.session_state["active_page"] = "❓ Quiz"
            st.rerun()
        return

    # Metrics Row
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
            <div class="stat-label">Accuracy ({total_q} Qs)</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        due_count = len(profile.get("due_reviews", []))
        due_color = "var(--warning)" if due_count > 0 else "var(--success)"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color: {due_color};">{due_count}</div>
            <div class="stat-label">Spaced Reviews Due</div>
        </div>
        """, unsafe_allow_html=True)

    rec = profile.get("primary_recommendation")
    if rec:
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="black-card" style="border-left: 3px solid #FFFFFF;">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 6px;">
                ⚡ Recommended Next Activity
            </div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">
                {rec.get('recommended_activity').replace('_', ' ').title()} on <u>{rec.get('topic')}</u> ({rec.get('recommended_difficulty').upper()} Difficulty)
            </div>
            <div style="background: #09090B; border: 1px solid var(--border-subtle); padding: 12px 14px; border-radius: 8px; font-size: 0.88rem; color: #D4D4D8; line-height: 1.5; margin-bottom: 12px;">
                <b>Pedagogical Reason:</b> {rec.get('reasoning')}
            </div>
            <div style="font-size: 0.80rem; color: var(--text-muted);">
                🎯 Goal: {rec.get('pedagogical_goal')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        rec_act = rec.get("recommended_activity", "quiz_practice")
        rec_top = rec.get("topic", "")
        rec_diff = rec.get("recommended_difficulty", "medium")
        if st.button(f"🚀 Start Recommended Activity: {rec_top} ({rec_diff.title()})", type="primary", use_container_width=True, key="btn_start_rec"):
            if "quiz" in rec_act:
                st.session_state["qz_mode"] = "topic"
                st.session_state["qz_topic"] = rec_top
                st.session_state["qz_diff"] = rec_diff
                st.session_state["active_page"] = "❓ Quiz"
            elif "flashcard" in rec_act:
                st.session_state["fc_mode"] = "topic"
                st.session_state["fc_topic"] = rec_top
                st.session_state["active_page"] = "🃏 Flashcards"
            else:
                st.session_state["active_page"] = "📝 Study Notes"
            st.rerun()

    weaknesses = profile.get("weaknesses", [])
    if weaknesses:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("### 🔍 Diagnostic Cognitive Alerts")
        for w in weaknesses:
            p_type = w.get("pattern_type").replace("_", " ").title()
            border = "rgba(239, 68, 68, 0.5)" if w.get("severity") == "high" else "rgba(245, 158, 11, 0.5)"
            st.markdown(f"""
            <div class="black-card" style="border-left: 3px solid {border}; padding: 14px 18px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #FFFFFF; font-size: 0.95rem;">
                        ⚠️ {p_type} — {w.get('topic')}
                    </span>
                    <span style="font-size: 0.70rem; font-weight: 700; text-transform: uppercase; color: {'var(--danger)' if w.get('severity')=='high' else 'var(--warning)'};">
                        {w.get('severity')} priority
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin: 6px 0;">
                    {w.get('summary')}
                </div>
                <div style="font-size: 0.82rem; color: var(--success);">
                    💡 {w.get('actionable_tip')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    topics = profile.get("topic_profiles", {})
    if topics:
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📊 Topic Knowledge Modeling")
        for t_name, t_data in topics.items():
            status = t_data.get("learning_status", "developing")
            badge_class = f"badge-{status}" if status in ("mastered", "struggling", "developing") else "badge-developing"
            mastery = t_data.get("mastery_score", 0.0)
            bkt = t_data.get("bkt_p_known", 0.20) * 100.0

            st.markdown(f"""
            <div class="black-card" style="padding: 16px 20px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <span style="font-size: 1.05rem; font-weight: 600; color: #FFFFFF;">{t_name}</span>
                        <span class="badge {badge_class}" style="margin-left: 8px;">{status}</span>
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF;">
                        {mastery:.0f}%
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 0.82rem; color: var(--text-secondary);">
                    <div>🧠 BKT: <b>{bkt:.1f}%</b></div>
                    <div>🟢 Easy: <b>{t_data.get('easy_accuracy', 0):.0f}%</b></div>
                    <div>🟡 Med: <b>{t_data.get('medium_accuracy', 0):.0f}%</b></div>
                    <div>🔴 Hard: <b>{t_data.get('hard_accuracy', 0):.0f}%</b></div>
                </div>
                <div style="margin-top: 8px; font-size: 0.76rem; color: var(--text-muted); display: flex; justify-content: space-between;">
                    <span>🔥 Streak: <b>{t_data.get('consecutive_correct', 0)}</b> correct</span>
                    <span>⏳ Next Review: <b>{t_data.get('next_review', 'N/A')[:10] if t_data.get('next_review') else 'N/A'}</b> (Interval: {t_data.get('interval_days', 1)}d)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    try:
        path_res = requests.get(f"{BACKEND_URL}/learning/path/{st.session_state['session_id']}/{active_doc_id}", timeout=10)
        if path_res.status_code == 200:
            path_data = path_res.json()
            nodes = path_data.get("nodes", [])
            if nodes:
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                st.markdown("### 🗺️ Adaptive Prerequisite Learning Path")
                st.markdown(
                    f"<div style='font-size: 0.82rem; color: var(--text-muted); margin-bottom: 14px;'>"
                    f"Progression gates subsequent concepts until prerequisite mastery reaches 60%. "
                    f"Completed: <b>{path_data.get('completed_topics_count', 0)}/{path_data.get('total_topics_count', len(nodes))}</b> modules."
                    f"</div>",
                    unsafe_allow_html=True,
                )

                for node in nodes:
                    n_status = node.get("status", "ready")
                    n_mastery = node.get("mastery_score", 0.0)
                    n_bkt = node.get("bkt_p_known", 0.20) * 100.0
                    n_unlocked = node.get("is_unlocked", True)
                    n_prereqs = node.get("prerequisites", [])

                    if n_status == "mastered":
                        status_badge = '<span class="badge badge-mastered">🏆 Mastered</span>'
                        status_border = "var(--success)"
                    elif n_status == "in_progress":
                        status_badge = '<span class="badge badge-developing">⚡ In Progress</span>'
                        status_border = "var(--accent-glow)"
                    elif n_status == "review_due":
                        status_badge = '<span class="badge badge-struggling">⏳ Review Due</span>'
                        status_border = "var(--warning)"
                    elif n_status == "locked":
                        status_badge = '<span class="badge" style="background:#27272A; color:#A1A1AA;">🔒 Locked</span>'
                        status_border = "#27272A"
                    else:
                        status_badge = '<span class="badge" style="background:#1E293B; color:#60A5FA;">🔓 Unlocked</span>'
                        status_border = "rgba(96, 165, 250, 0.4)"

                    prereq_text = f"Prerequisite: <i>{', '.join(n_prereqs)}</i> (min 60% mastery)" if n_prereqs else "Foundational module (No prerequisites)"

                    st.markdown(f"""
                    <div class="black-card" style="border-left: 3px solid {status_border}; padding: 16px 20px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <div>
                                <span style="font-size: 0.74rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Step {node.get('order_index', 1)}</span>
                                <span style="font-size: 1.05rem; font-weight: 600; color: #FFFFFF; margin-left: 8px;">{node.get('topic')}</span>
                            </div>
                            <div>{status_badge}</div>
                        </div>
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 8px;">
                            {prereq_text}
                        </div>
                        <div style="display: flex; gap: 20px; font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 8px;">
                            <span>Mastery: <b>{n_mastery:.0f}%</b></span>
                            <span>BKT Knowledge: <b>{n_bkt:.1f}%</b></span>
                        </div>
                        <div style="font-size: 0.82rem; color: #D4D4D8;">
                            🎯 <b>Next step:</b> {node.get('recommended_next_step', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if n_unlocked:
                        if st.button(f"🎯 Practice '{node.get('topic')}'", key=f"btn_path_topic_{node.get('order_index')}"):
                            st.session_state["qz_mode"] = "topic"
                            st.session_state["qz_topic"] = node.get("topic")
                            st.session_state["qz_diff"] = "easy" if n_mastery < 40 else ("medium" if n_mastery < 75 else "hard")
                            st.session_state["active_page"] = "❓ Quiz"
                            st.rerun()
    except Exception:
        pass


def render_quiz_page(active_doc_id):
    st.markdown("""
    <div style="padding: 10px 0 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 20px;">
        <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">Multiple Choice Assessment</span>
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;">
            Auto-generated quizzes with confidence rating and automated Bayesian Knowledge Tracing sync.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not active_doc_id:
        st.info("Select or upload a PDF document in the sidebar to generate a quiz.")
        return

    if "qz_diff" not in st.session_state:
        st.session_state["qz_diff"] = "medium"
    if "qz_mode" not in st.session_state:
        st.session_state["qz_mode"] = "full_document"
    if "qz_topic" not in st.session_state:
        st.session_state["qz_topic"] = ""
    if "qz_count" not in st.session_state:
        st.session_state["qz_count"] = 5

    qc1, qc2, qc3, qc4 = st.columns([1, 1, 1, 1])
    with qc1:
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], key="qz_diff")
    with qc2:
        q_mode = st.selectbox("Scope", ["full_document", "topic"], key="qz_mode")
    with qc3:
        q_topic = st.text_input("Topic", key="qz_topic", placeholder="(optional)")
    with qc4:
        num_q = st.number_input("Questions", min_value=1, max_value=20, key="qz_count")

    if st.button("Generate Quiz", type="primary"):
        with st.spinner("Generating questions…"):
            payload = {
                "document_id": active_doc_id,
                "difficulty": difficulty,
                "generation_mode": q_mode,
                "topic": q_topic if q_mode == "topic" else None,
                "num_questions": num_q,
            }
            try:
                res = requests.post(f"{BACKEND_URL}/quiz/", json=payload, timeout=45)
                if res.status_code == 200:
                    st.session_state["quiz_questions"] = res.json().get("questions", [])
                    st.session_state["quiz_submitted"] = False
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_confidences"] = {}
                    st.rerun()
                else:
                    st.error(f"Failed to generate quiz questions ({res.status_code}): {get_api_error(res)}")
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
                    <div class="quiz-card">
                        <div style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px;">
                            Question {i + 1} of {len(questions)} &nbsp;·&nbsp; {q.get('topic', 'General')}
                        </div>
                        <div style="font-size: 1.05rem; font-weight: 600; color: #FFFFFF; margin-bottom: 12px;">
                            {q['question']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    user_answers[i] = st.radio(
                        f"Select answer Q{i + 1}",
                        options=q["options"],
                        key=f"q_{i}",
                        label_visibility="collapsed",
                    )
                    user_confidences[i] = st.slider(
                        f"Confidence rating (Q{i + 1})",
                        min_value=10,
                        max_value=100,
                        value=70,
                        step=10,
                        key=f"conf_{i}",
                        help="Helps the Adaptive Engine calibrate your metacognition and detect misconceptions.",
                    )

                if st.form_submit_button("Submit Assessment", use_container_width=True):
                    st.session_state["quiz_answers"] = user_answers
                    st.session_state["quiz_confidences"] = user_confidences
                    st.session_state["quiz_submitted"] = True

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

                border = "var(--success)" if is_correct else "var(--danger)"
                icon = "✅" if is_correct else "❌"
                conf_val = user_confidences.get(i, 70)

                calib_badge = ""
                if not is_correct and conf_val >= 70:
                    calib_badge = '<span style="color:var(--danger); font-size:0.75rem; font-weight:600;">⚠️ Potential Misconception (High Confidence Mistake)</span>'
                elif is_correct and conf_val <= 40:
                    calib_badge = '<span style="color:var(--text-muted); font-size:0.75rem; font-weight:600;">💡 Tentative Recall (Low Confidence Success)</span>'

                st.markdown(f"""
                <div class="quiz-card" style="border-left: 3px solid {border};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-muted);">{icon} Question {i + 1} &nbsp;·&nbsp; {q.get('topic', 'General')}</div>
                        {calib_badge}
                    </div>
                    <div style="font-size: 1.0rem; font-weight: 600; color: #FFFFFF; margin-bottom: 8px;">{q['question']}</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">
                        Your answer: <b>{selected}</b> ({conf_val}% confidence)<br/>
                        Correct answer: <b style="color: var(--success);">{correct_option}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            pct = int((score / total) * 100)
            st.markdown(f"""
            <div class="black-card" style="text-align: center; margin-top: 20px;">
                <div style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF;">{pct}%</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #FFFFFF; margin: 4px 0;">{score} / {total} Correct</div>
                <div style="font-size: 0.82rem; color: var(--text-muted);">
                    Learner model & BKT states updated automatically.
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_retake, col_adapt = st.columns(2)
            with col_retake:
                if st.button("Retake Quiz", use_container_width=True):
                    st.session_state["quiz_submitted"] = False
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_confidences"] = {}
                    st.rerun()
            with col_adapt:
                if st.button("View Adaptive Knowledge Profile", type="primary", use_container_width=True):
                    st.session_state["active_page"] = "🎯 Adaptive Engine"
                    st.rerun()


def render_flashcards_page(active_doc_id):
    st.markdown("""
    <div style="padding: 10px 0 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 20px;">
        <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">Interactive Flashcards</span>
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;">
            Spaced repetition question & answer cards for active recall.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not active_doc_id:
        st.info("Select or upload a PDF document in the sidebar to generate flashcards.")
        return

    if "fc_mode" not in st.session_state:
        st.session_state["fc_mode"] = "full_document"
    if "fc_topic" not in st.session_state:
        st.session_state["fc_topic"] = ""
    if "fc_count" not in st.session_state:
        st.session_state["fc_count"] = 5

    fc1, fc2, fc3 = st.columns([2, 2, 1])
    with fc1:
        gen_mode = st.selectbox("Scope", ["full_document", "topic"], key="fc_mode")
    with fc2:
        topic_input = st.text_input("Topic (if scope = topic)", key="fc_topic", placeholder="e.g. Relational Model")
    with fc3:
        num_cards = st.number_input("Count", min_value=1, max_value=20, key="fc_count")

    if st.button("Generate Deck", type="primary"):
        with st.spinner("Creating flashcards…"):
            payload = {
                "document_id": active_doc_id,
                "generation_mode": gen_mode,
                "topic": topic_input if gen_mode == "topic" else None,
                "num_flashcards": num_cards,
            }
            try:
                res = requests.post(f"{BACKEND_URL}/flashcards/", json=payload, timeout=45)
                if res.status_code == 200:
                    st.session_state["flashcards"] = res.json().get("questions", [])
                    st.session_state["flashcard_idx"] = 0
                    st.session_state["show_card_answer"] = False
                    st.rerun()
                else:
                    st.error(f"Failed to generate flashcards ({res.status_code}): {get_api_error(res)}")
            except Exception as e:
                st.error(f"Error: {e}")

    cards = st.session_state["flashcards"]
    if cards:
        idx = st.session_state["flashcard_idx"]
        card = cards[idx]
        is_answer = st.session_state["show_card_answer"]
        label = "ANSWER" if is_answer else "QUESTION"
        content = card["answer"] if is_answer else card["question"]
        topic_label = card.get("topic", "")

        st.markdown(f"<div style='text-align: center; color: var(--text-muted); font-size: 0.82rem; margin-bottom: 12px;'>Card {idx + 1} of {len(cards)}</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="flashcard-face">
            <div class="flashcard-label">{label}{(' · ' + topic_label) if topic_label else ''}</div>
            <div class="flashcard-text">{content}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button("⬅️ Previous", use_container_width=True, disabled=(idx == 0)):
                st.session_state["flashcard_idx"] -= 1
                st.session_state["show_card_answer"] = False
                st.rerun()
        with nav2:
            flip_label = "Show Question" if is_answer else "Reveal Answer"
            if st.button(flip_label, use_container_width=True, type="primary"):
                st.session_state["show_card_answer"] = not is_answer
                st.rerun()
        with nav3:
            if st.button("Next ➡️", use_container_width=True, disabled=(idx >= len(cards) - 1)):
                st.session_state["flashcard_idx"] += 1
                st.session_state["show_card_answer"] = False
                st.rerun()


def render_notes_page(active_doc_id):
    active_meta = st.session_state["documents"].get(active_doc_id) if active_doc_id else None
    doc_name = active_meta["filename"] if active_meta else "document"

    st.markdown("""
    <div style="padding: 10px 0 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 20px;">
        <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">AI Study Notes</span>
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;">
            Structured revision notes summarizing key definitions, formulas, and concepts.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not active_doc_id:
        st.info("Select or upload a PDF document in the sidebar to generate notes.")
        return

    if st.button("Generate Study Notes", type="primary"):
        with st.spinner("Synthesizing notes…"):
            try:
                res = requests.post(f"{BACKEND_URL}/notes/{active_doc_id}", timeout=60)
                if res.status_code == 200:
                    st.session_state["notes_content"] = res.json().get("notes", "")
                else:
                    st.error(f"Failed to generate notes ({res.status_code}): {get_api_error(res)}")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state["notes_content"]:
        st.markdown(f"""
        <div class="black-card" style="line-height: 1.7; padding: 28px;">
            {st.session_state["notes_content"]}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Raw Markdown Source", expanded=False):
            st.code(st.session_state["notes_content"], language="markdown")

        st.download_button(
            "Download Notes (.md)",
            st.session_state["notes_content"],
            file_name=f"{doc_name}_notes.md",
        )


def render_topics_page(active_doc_id):
    st.markdown("""
    <div style="padding: 10px 0 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 20px;">
        <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">Key Document Topics</span>
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;">
            Automatic extraction of core conceptual themes and topic structures.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not active_doc_id:
        st.info("Select or upload a PDF document in the sidebar to extract topics.")
        return

    if st.button("Extract Topics", type="primary"):
        with st.spinner("Discovering topics…"):
            try:
                res = requests.post(f"{BACKEND_URL}/topics/{active_doc_id}", timeout=45)
                if res.status_code == 200:
                    st.session_state["topics_list"] = res.json().get("topics", [])
                else:
                    st.error(f"Failed to extract topics ({res.status_code}): {get_api_error(res)}")
            except Exception as e:
                st.error(f"Error: {e}")

    topics = st.session_state["topics_list"]
    if topics:
        st.markdown(f"<div style='font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;'>Discovered {len(topics)} topics</div>", unsafe_allow_html=True)
        for t in topics:
            st.markdown(f"""
            <div class="black-card" style="padding: 16px 20px; margin-bottom: 10px;">
                <div style="font-size: 1.05rem; font-weight: 600; color: #FFFFFF; margin-bottom: 4px;">
                    📌 {t.get('name', 'Topic')}
                </div>
                <div style="font-size: 0.86rem; color: var(--text-secondary); line-height: 1.5;">
                    {t.get('description', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)


active_doc_id = st.session_state["active_doc_id"]
current_page = st.session_state["active_page"]

if current_page == "💬 Chat":
    render_chat_page(active_doc_id)
elif current_page == "🎯 Adaptive Engine":
    render_adaptive_page(active_doc_id)
elif current_page == "❓ Quiz":
    render_quiz_page(active_doc_id)
elif current_page == "🃏 Flashcards":
    render_flashcards_page(active_doc_id)
elif current_page == "📝 Study Notes":
    render_notes_page(active_doc_id)
elif current_page == "🗂️ Topics":
    render_topics_page(active_doc_id)
