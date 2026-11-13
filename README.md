# DocuMind 🧠
### Intelligent PDF Learning Platform with Adaptive Mastery & Cognitive Analytics

DocuMind is an end-to-end AI document intelligence and adaptive learning platform. It transforms static PDF documents into interactive study ecosystems using a Retrieval-Augmented Generation (RAG) pipeline, Bayesian Knowledge Tracing (BKT), SuperMemo (SM-2) Spaced Repetition, and automated pedagogical generators (Quizzes, Flashcards, Summaries, and Topic Roadmaps).

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Architecture & Data Flow](#-architecture--data-flow)
- [Adaptive Learning Engine](#-adaptive-learning-engine)
- [Tech Stack](#-tech-stack)
- [Project Directory Structure](#-project-directory-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running Backend & Frontend](#running-backend--frontend)
- [REST API Reference](#-rest-api-reference)
  - [Document Management](#document-management)
  - [Conversational RAG Chat](#conversational-rag-chat)
  - [Adaptive Learning Engine](#adaptive-learning-engine-endpoints)
  - [Study Notes Generator](#study-notes-generator)
  - [Topic Extraction](#topic-extraction)
  - [Quiz Assessment Generator](#quiz-assessment-generator)
  - [Flashcard Generator](#flashcard-generator)
- [Frontend Workspace Walkthrough](#-frontend-workspace-walkthrough)
- [Data Persistence](#-data-persistence)
- [License](#-license)

---

## 🌟 Key Features

| Module | Description |
|---|---|
| 📄 **Document Hub** | Multi-document upload, automatic PDF text extraction, chunking, embedding, and automatic session persistence across server reloads. |
| 💬 **Conversational RAG Chat** | Grounded Q&A powered by a history-aware RAG pipeline and `openai/gpt-oss-120b` via Groq, complete with 2x2 suggested question starters. |
| 🎯 **Adaptive Engine** | Real-time cognitive modeling using **Bayesian Knowledge Tracing (BKT)**, **SuperMemo (SM-2) Spaced Repetition**, confidence calibration, and error pattern diagnosis. |
| ❓ **Interactive Quiz System** | Configurable MCQ assessment generation (Easy, Medium, Hard; Full Document or Topic-scoped) with confidence tracking and instant automated grading. |
| 🃏 **Active Recall Flashcards** | Structured flip-card study deck with self-rating ("Needs Review" vs "Mastered") directly integrated with spaced repetition intervals. |
| 📝 **Map-Reduce Study Notes** | Hierarchical study guides generated via map-reduce summarization, distilling complex document chunks into structured key concepts. |
| 🗂️ **Automated Topic Catalog** | LLM-driven topic extraction with one-click shortcuts to launch topic-focused quizzes, flashcards, or targeted chat discussions. |

---

## 🏗 Architecture & Data Flow

```text
                               ┌─────────────────────────────┐
                               │       Uploaded PDF          │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │   PyPDF Text Extraction     │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │ RecursiveCharacterSplitter  │
                               │  (size=1000, overlap=200)   │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  HuggingFace MiniLM-L6-v2   │
                               │    (Dense 384-d Vectors)    │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │      ChromaDB Storage       │
                               │  (Collection per document)  │
                               └──────────────┬──────────────┘
                                              │
       ┌───────────────────┬──────────────────┼──────────────────┬───────────────────┐
       ▼                   ▼                  ▼                  ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌─────────────────┐
│ Conversational│   │  Map-Reduce  │   │    Topic     │   │     Quiz     │   │    Flashcard    │
│  RAG Chain   │   │ Summarization│   │  Extraction  │   │  Generator   │   │    Generator    │
│ (ChatGroq)   │   │ (ChatGroq)   │   │ (ChatGroq)   │   │ (ChatGroq)   │   │   (ChatGroq)    │
└──────┬───────┘   └──────────────┘   └──────────────┘   └──────┬───────┘   └────────┬────────┘
       │                                                        │                    │
       │                                                        ▼                    ▼
       │                                              ┌─────────────────────────────────────┐
       │                                              │      Adaptive Learning Engine       │
       │                                              │ ─────────────────────────────────── │
       │                                              │ • Bayesian Knowledge Tracing (BKT)  │
       │                                              │ • SuperMemo (SM-2) Spaced Repetition│
       │                                              │ • Confidence Calibration Detection  │
       │                                              │ • Conceptual Weakness Diagnosis     │
       │                                              │ • Prerequisite Learning Roadmap     │
       │                                              └──────────────────┬──────────────────┘
       │                                                                 │
       └───────────────────────────────┬─────────────────────────────────┘
                                       ▼
                       ┌───────────────────────────────┐
                       │   Streamlit Web Workspace     │
                       │   (Pure Black Modern UI)      │
                       └───────────────────────────────┘
```

---

## 🎯 Adaptive Learning Engine

DocuMind's standout capability is its quantitative pedagogical framework modeled after modern cognitive science:

### 1. Bayesian Knowledge Tracing (BKT)
Tracks latent knowledge state probability $P(L_t)$ for each extracted topic:
- **Prior Knowledge** ($P(L_0) = 0.20$): Initial baseline familiarity.
- **Transit Probability** ($P(T) = 0.15$): Likelihood of mastering a concept during a learning opportunity.
- **Slip Parameter** ($P(S)$): Probability of answering incorrectly despite knowing the material (scaled by difficulty: Easy $0.08$, Hard $0.15$).
- **Guess Parameter** ($P(G)$): Probability of guessing correctly without mastery (Easy $0.30$, Hard $0.15$, 4-option MCQ baseline $0.25$).

### 2. Spaced Repetition (SuperMemo SM-2)
Calculates optimal review intervals based on performance and user self-ratings:
- Dynamically adjusts the **Ease Factor** ($EF \ge 1.3$).
- Schedules retention reviews at $1 \text{ day} \to 6 \text{ days} \to I \times EF$.
- Highlights overdue topics in the dashboard to prevent memory decay.

### 3. Confidence Calibration & Error Diagnosis
Compares student self-reported confidence against actual question correctness:
- **Overconfidence**: High confidence with incorrect answers (identifies hazardous misconceptions).
- **Underconfidence / Imposter Phenomenon**: Correct answers with low confidence (prompts positive reinforcement).
- **Student A vs Student B Diagnosis**: Distinguishes between students struggling with advanced synthesis vs students making careless mistakes on fundamental questions.

### 4. Adaptive Prerequisite Roadmap
Generates a prerequisite dependency tree across document topics, gating advanced sections until foundational topic mastery reaches threshold ($\ge 70\%$).

---

## 🛠 Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** — Asynchronous REST API framework.
- **[LangChain](https://www.langchain.com/)** & **[LangChain Community](https://python.langchain.com/)** — LLM orchestration, document chains, and conversational memory.
- **[LangChain Groq](https://python.langchain.com/docs/integrations/chat/groq/)** — Ultra-fast inference using `openai/gpt-oss-120b` via Groq.
- **[ChromaDB](https://www.trychroma.com/)** — Local, persistent vector store.
- **[HuggingFace Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)** — Dense 384-dimensional vector embeddings using `all-MiniLM-L6-v2`.
- **[PyPDF](https://pypdf.readthedocs.io/)** — Robust PDF text parsing and metadata extraction.
- **[Pydantic v2](https://docs.pydantic.dev/)** & **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** — Data validation and environment settings management.
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI web server.

### Frontend
- **[Streamlit](https://streamlit.io/)** — Interactive reactive web client.
- **Custom Design System** — Tailored pure black theme (`#000000` canvas, `#121214` cards, `#27272A` borders, Inter typography, responsive 900px centered workspaces).
- **Requests** — Synchronous and streaming client communication with backend endpoints.

---

## 📁 Project Directory Structure

```text
DocuMind/
├── .streamlit/
│   └── config.toml               # Streamlit theme configuration (Pure Black #000000)
├── backend/
│   └── app/
│       ├── main.py               # FastAPI entry point & router mounting
│       ├── config.py             # Settings (Groq API key, paths) via Pydantic
│       ├── api/
│       │   └── routes/
│       │       ├── documents.py  # POST /documents/upload
│       │       ├── chat.py       # POST /chats/chat
│       │       ├── learning.py   # POST & GET /learning/* (Adaptive Engine)
│       │       ├── notes.py      # POST /notes/{document_id}
│       │       ├── topics.py     # POST /topics/{document_id}
│       │       ├── quiz.py       # POST /quiz/
│       │       └── flashcards.py # POST /flashcards/
│       ├── services/
│       │   ├── document_services.py  # PDF processing & pipeline coordination
│       │   ├── chunk_service.py      # RecursiveCharacterTextSplitter configuration
│       │   ├── embedding_services.py # HuggingFace embedding & ChromaDB CRUD
│       │   ├── rag_services.py       # History-aware conversational RAG chain
│       │   ├── learning_service.py   # BKT, SM-2, and cognitive diagnostic engine
│       │   ├── notes_service.py      # Map-reduce summarization chain
│       │   ├── topic_service.py      # LLM-based structured topic extraction
│       │   ├── quiz_service.py       # Structured MCQ quiz generation
│       │   └── flashcard_service.py  # Structured flashcard generator
│       └── schemas/
│           ├── document.py       # DocumentResponse schema
│           ├── chat.py           # ChatRequest schema
│           ├── learning.py       # QuestionAttempt, LearnerProfile, LearningPath
│           ├── quiz.py           # QuizRequest, QuizResponse, QuestionSchema
│           └── flashcards.py     # FlashCardRequest, FlashCardResponse
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml           # Frontend-local Streamlit configuration
│   └── app.py                    # Complete multi-tab Streamlit frontend
├── data/
│   ├── uploads/                  # Uploaded PDF files (<document_id>.pdf)
│   ├── chroma_db/                # Persisted ChromaDB vector collections
│   └── learner_profiles/         # Stored JSON learner models (<session>_<doc>.json)
├── requirements.txt              # Project Python dependencies
├── .env                          # Local environment variables (API keys)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- A **[Groq API Key](https://console.groq.com/)** (for high-speed LLM inference)
- A **[HuggingFace Access Token](https://huggingface.co/settings/tokens)** (for downloading sentence transformers)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd DocuMind
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
HF_TOKEN=hf_your_huggingface_token_here
```

> [!WARNING]
> Never commit your `.env` file to version control. It is already excluded in `.gitignore`.

### Running Backend & Frontend

DocuMind runs as a two-tier application: FastAPI for backend AI services and Streamlit for the user interface.

#### 1. Start the FastAPI Backend
```bash
uvicorn backend.app.main:app --reload --port 8000
```
- API Endpoint: `http://127.0.0.1:8000`
- Interactive Swagger Documentation: `http://127.0.0.1:8000/docs`
- Redoc Documentation: `http://127.0.0.1:8000/redoc`

#### 2. Start the Streamlit Frontend
In a separate terminal (with the virtual environment activated):
```bash
streamlit run frontend/app.py
```
- The application will automatically open in your default browser at `http://localhost:8501`.

---

## 📡 REST API Reference

### Document Management

#### `POST /documents/upload`
Uploads and indexes a new PDF document.

- **Request:** `multipart/form-data` with key `file` (must be `application/pdf`).
- **Response `200 OK`:**
  ```json
  {
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "filename": "Research_Paper.pdf",
    "content_type": "application/pdf",
    "file_size": 102713,
    "page_count": 5,
    "title": "Research on Alternative Data",
    "chunks_size": 18,
    "status": "uploaded"
  }
  ```

---

### Conversational RAG Chat

#### `POST /chats/chat`
Ask contextual questions against the uploaded PDF document with per-session conversational history.

- **Request Body:**
  ```json
  {
    "session_id": "session-12345",
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "question": "What is the primary conclusion regarding alternative data?"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "session_id": "session-12345",
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "question": "What is the primary conclusion regarding alternative data?",
    "answer": "The primary conclusion indicates that incorporating alternative data yields significant alpha..."
  }
  ```

---

### Adaptive Learning Engine Endpoints

#### `POST /learning/attempt`
Logs a single question attempt, immediately calculating BKT and SM-2 updates.

- **Request Body:**
  ```json
  {
    "topic": "Neural Networks",
    "difficulty": "medium",
    "is_correct": true,
    "confidence": 85.0,
    "time_spent_seconds": 18.5,
    "question_text": "What is backpropagation?",
    "user_answer": "Option B",
    "correct_answer": "Option B"
  }
  ```
- **Query Params:** `?session_id=...&document_id=...`
- **Response `200 OK`:**
  ```json
  {
    "status": "success",
    "topic": "Neural Networks",
    "mastery_score": 78.4,
    "bkt_p_known": 0.82,
    "learning_status": "mastered",
    "calibration_status": "well_calibrated",
    "next_review": "2026-11-19T10:00:00Z"
  }
  ```

#### `POST /learning/submit-quiz`
Batch submits all questions from a completed quiz assessment, recomputes global mastery, and detects cognitive error patterns.

- **Request Body:**
  ```json
  {
    "session_id": "session-12345",
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "attempts": [
      {
        "topic": "Backpropagation",
        "difficulty": "hard",
        "is_correct": false,
        "confidence": 90.0
      }
    ]
  }
  ```
- **Response `200 OK`:** Full `LearnerProfileResponse` object.

#### `GET /learning/profile/{session_id}/{document_id}`
Returns complete multidimensional learner metrics: overall mastery score, BKT probabilities, difficulty-level accuracy breakdown, detected weakness patterns, and overdue reviews.

#### `GET /learning/recommendation/{session_id}/{document_id}`
Returns the recommended next study action (e.g. `notes_review`, `quiz_practice`, `flashcard_revision`) with pedagogical justification.

#### `GET /learning/path/{session_id}/{document_id}`
Returns the adaptive prerequisite learning roadmap with unlock statuses.

---

### Study Notes Generator

#### `POST /notes/{document_id}`
Triggers a Map-Reduce summarization chain to construct structured study notes.

- **Response `200 OK`:**
  ```json
  {
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "notes": "## Key Takeaways\n\n- Definition of alternative data...\n- Core findings...",
    "status": "success"
  }
  ```

---

### Topic Extraction

#### `POST /topics/{document_id}`
Extracts key topics and concepts from the document.

- **Response `200 OK`:**
  ```json
  {
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "topics": [
      {
        "name": "Alternative Data Sources",
        "description": "Unconventional data sets used to gain financial insights."
      }
    ],
    "total_topics": 1,
    "status": "success"
  }
  ```

---

### Quiz Assessment Generator

#### `POST /quiz/`
Generates a structured multiple-choice quiz.

- **Request Body:**
  ```json
  {
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "difficulty": "medium",
    "generation_mode": "full_document",
    "topic": null,
    "num_questions": 5
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "questions": [
      {
        "question": "Which of the following describes alternative data?",
        "options": [
          "Standard balance sheet data",
          "Satellite imagery and web scraping metrics",
          "Historical stock prices",
          "Government treasury yields"
        ],
        "correct_answer": "Satellite imagery and web scraping metrics",
        "topic": "Alternative Data Sources"
      }
    ]
  }
  ```

---

### Flashcard Generator

#### `POST /flashcards/`
Generates interactive Q&A flashcards.

- **Request Body:**
  ```json
  {
    "document_id": "cace23cb-833f-4006-b51a-9bb582028c13",
    "generation_mode": "full_document",
    "topic": null,
    "num_flashcards": 5
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "questions": [
      {
        "question": "What is the primary benefit of alternative data in investment modeling?",
        "answer": "It provides non-traditional signals that precede conventional quarterly earnings reports.",
        "topic": "Alternative Data Sources"
      }
    ]
  }
  ```

---

## 🖥 Frontend Workspace Walkthrough

The DocuMind frontend provides a sleek, cohesive pure-black dark workspace with zero visual clutter:

1. **Sidebar Hub**:
   - **Upload PDF**: Immediate client-side file upload and server ingestion.
   - **Active Document Selector**: Displays the currently selected document and automatically recovers persisted documents across browser reloads.
   - **Workspace Navigation**: Fast switching between all 6 core study modules.
   - **Clear Chat**: One-click reset for session conversation history.

2. **💬 Chat Workspace**:
   - Anchored, centered question bar matching the exact canvas background.
   - 2x2 suggested question prompts for rapid exploration.
   - Full conversational streaming with clear user and assistant bubbles.

3. **🎯 Adaptive Engine Workspace**:
   - Visual overall mastery progress metric.
   - Topic Mastery Breakdown cards showing BKT $P(L_t)$ percentages, attempt counts, and status badges (`Mastered`, `Developing`, `Struggling`).
   - Difficulty Breakdown meters (Easy, Medium, Hard).
   - Metacognitive Calibration analysis (identifying overconfidence vs underconfidence).
   - Spaced Repetition agenda showing upcoming and overdue card reviews.

4. **❓ Quiz Workspace**:
   - Customizable parameters: choose difficulty (`Easy`, `Medium`, `Hard`) and scope (`Full Document` or `Specific Topic`).
   - Confidence slider for each question to feed calibration analytics.
   - Instant scoring with visual explanations and one-click submission into the learner profile.

5. **🃏 Flashcard Workspace**:
   - Clean card-flipper UI for quick-fire concept reviews.
   - Rating buttons ("Need Review" vs "Mastered") that calibrate future SM-2 intervals.

6. **📝 Study Notes & 🗂️ Topics Workspaces**:
   - Instant one-click generation of formatted markdown study guides.
   - Interactive topic matrix with direct shortcuts to quiz or chat about specific concepts.

---

## 💾 Data Persistence

DocuMind keeps data organized and separated across three dedicated local directories:

| Storage Location | Purpose | Format | Persistence Behavior |
|---|---|---|---|
| `data/uploads/` | Uploaded raw PDF files | `<document_id>.pdf` | Permanent on disk |
| `data/chroma_db/` | Vector database index & chunk embeddings | SQLite + binary vectors | Permanent on disk |
| `data/learner_profiles/` | Cognitive learner profiles & BKT states | `<session>_<doc>.json` | Permanent on disk |

---

## 📄 License

This project is licensed under the MIT License. Feel free to use and extend it for academic, personal, or commercial applications.
