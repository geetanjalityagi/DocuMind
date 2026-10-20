
import streamlit as st
import requests 
import uuid

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="DocuMind — Interactive Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING FOR MODERN UI ---
st.markdown("""
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        border-radius: 8px 8px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6366F1 !important;
        color: white !important;
    }
    .flashcard {
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "documents" not in st.session_state:
    st.session_state["documents"] = {}  # doc_id: filename
if "active_doc_id" not in st.session_state:
    st.session_state["active_doc_id"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "flashcards" not in st.session_state:
    st.session_state["flashcards"] = []
if "flashcard_idx" not in st.session_state:
    st.session_state["flashcard_idx"] = 0
if "show_card_answer" not in st.session_state:
    st.session_state["show_card_answer"] = False

# --- SIDEBAR: DOCUMENT HUB ---
with st.sidebar:
    st.title("🧠 DocuMind Hub")
    st.caption("AI-Powered PDF Intelligence")
    
    st.divider()
    
    # 1. Document Upload
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Ingest Document", type="primary", use_container_width=True):
            with st.spinner("Parsing, chunking, and embedding..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    res = requests.post(f"{BACKEND_URL}/documents/upload", files=files)
                    if res.status_code == 200:
                        data = res.json()
                        doc_id = data["document_id"]
                        st.session_state["documents"][doc_id] = data["filename"]
                        st.session_state["active_doc_id"] = doc_id
                        st.success(f"Successfully processed: {data['filename']}")
                    else:
                        st.error("Upload failed. Check backend logs.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")

    # 2. Document Selection
    if st.session_state["documents"]:
        st.divider()
        st.subheader("📚 Active Document")
        doc_options = list(st.session_state["documents"].keys())
        selected_id = st.selectbox(
            "Select Document",
            options=doc_options,
            format_func=lambda x: st.session_state["documents"][x],
            index=doc_options.index(st.session_state["active_doc_id"]) if st.session_state["active_doc_id"] in doc_options else 0
        )
        st.session_state["active_doc_id"] = selected_id

    st.divider()
    st.caption(f"Session ID: `{st.session_state['session_id'][:8]}...`")