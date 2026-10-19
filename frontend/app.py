
import streamlit as st

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# Must be the first Streamlit command
# --------------------------------------------------

st.set_page_config(
    page_title="DocuMind | AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# 2. CUSTOM THEME / CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Main application background */
    .stApp {
        background-color: #F7F8FC;
        color: #172746;
    }

    /* Main content spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #172746;
        border-right: 1px solid #263957;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    /* Sidebar navigation options */
    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 0.45rem;
    }

    [data-testid="stSidebar"] [role="radio"] {
        background-color: transparent;
        padding: 0.75rem 0.85rem;
        border-radius: 10px;
        border: 1px solid transparent;
    }

    [data-testid="stSidebar"] [role="radio"]:hover {
        background-color: #263957;
    }

    /* Buttons */
    .stButton > button {
        background-color: #4F46E5;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1rem;
        font-weight: 600;
        transition: background-color 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #4338CA;
        color: white;
        border: none;
    }

    /* Inputs and select boxes */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px;
    }

    /* Cards and containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

    /* Hide Streamlit's default menu and footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Divider */
    hr {
        border-color: #E5E7EB;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 3. SIDEBAR BRANDING
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 8px 4px 20px 4px;">
            <h1 style="
                font-size: 42px;
                margin: 0;
                font-weight: 750;
                letter-spacing: -1px;
            ">
                📚 DocuMind
            </h1>
            <p style="
                font-size: 15px;
                color: #B8C5D9;
                margin-top: 5px;
            ">
                Your AI-powered study companion
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        "<p style='font-size:12px; color:#AAB9D0; "
        "font-weight:700; letter-spacing:1px;'>WORKSPACE</p>",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------
    # 4. SIDEBAR NAVIGATION
    # --------------------------------------------------

    pages = {
        "🏠  Home": "Home",
        "📤  Upload PDF": "Upload PDF",
        "💬  Chat with PDF": "Chat with PDF",
        "📝  Study Notes": "Study Notes",
        "🎯  Quiz": "Quiz",
        "🗂️  Flashcards": "Flashcards",
    }

    selected_page = st.radio(
        "Navigation",
        options=list(pages.keys()),
        label_visibility="collapsed",
        key="selected_page",
    )

    st.divider()

    # Small sidebar footer
    st.markdown(
        """
        <div style="
            padding: 12px 4px;
            font-size: 12px;
            color: #B8C5D9;
            line-height: 1.8;
        ">
            <b style="color:#FFFFFF;">Study smarter, not harder.</b>
            <br>
            Upload your documents and turn them into learning resources.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# 5. PAGE ROUTING
# --------------------------------------------------

current_page = pages[selected_page]

if current_page == "Home":
    st.title("Welcome to StudyMind 👋")
    st.write(
        "Your personal AI study space. Upload a PDF to get started."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("📤 Upload PDF")
            st.write("Upload your study material and prepare it for learning.")
            if st.button("Upload a document", key="home_upload", use_container_width=True):
                st.session_state["selected_page"] = "📤  Upload PDF"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("💬 Chat with PDF")
            st.write("Ask questions and understand your document.")
            if st.button("Start chatting", key="home_chat", use_container_width=True):
                st.session_state["selected_page"] = "💬  Chat with PDF"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.subheader("🗂️ Flashcards")
            st.write("Revise important concepts with AI-generated flashcards.")
            if st.button("Study flashcards", key="home_flashcards", use_container_width=True):
                st.session_state["selected_page"] = "🗂️  Flashcards"
                st.rerun()

    st.divider()
    st.subheader("Your learning workspace")
    st.info(
        "Your uploaded documents and recent activity will appear here "
        "when we connect the document management functionality."
    )

elif current_page == "Upload PDF":
    st.title("📤 Upload your study material")
    st.write("Upload a PDF to start learning with StudyMind.")
    st.info("The PDF upload interface will be implemented in the next step.")

elif current_page == "Chat with PDF":
    st.title("💬 Chat with your document")
    st.write("Ask questions and get answers grounded in your PDF.")
    st.info("The document chat interface will be implemented next.")

elif current_page == "Study Notes":
    st.title("📝 Generate study notes")
    st.write("Turn lengthy documents into clear, structured notes.")
    st.info("The notes generation interface will be implemented next.")

elif current_page == "Quiz":
    st.title("🎯 Test your knowledge")
    st.write("Generate quizzes and check your understanding.")
    st.info("The quiz interface will be implemented next.")

elif current_page == "Flashcards":
    st.title("🗂️ AI Flashcards")
    st.write("Revise concepts using question-and-answer flashcards.")
    st.info("The flashcard interface will be connected to your existing backend next.")
