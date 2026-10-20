# DocuMind 🧠

DocuMind is an AI-powered document intelligence platform that transforms static PDF documents into interactive learning experiences. Upload a PDF and instantly unlock contextual Q&A, auto-generated study notes, flashcards, quizzes, and topic extraction — all powered by a Retrieval-Augmented Generation (RAG) pipeline.

---

## Features

| Feature | Description |
|---|---|
| 📄 **Document Upload** | Upload PDF files; text is extracted, chunked, and embedded into a persistent vector store |
| 💬 **Conversational Q&A** | Chat with your document using a history-aware RAG pipeline |
| 📝 **Auto Notes** | Generate comprehensive study notes using a map-reduce summarization chain |
| 🗂️ **Topic Extraction** | Automatically identify and list the main topics covered in a document |
| 🃏 **Flashcard Generation** | Create Q&A flashcards from the full document or a specific topic |
| ❓ **Quiz Generation** | Generate multiple-choice quizzes with configurable difficulty and scope |

---

## Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** — Async REST API framework
- **[LangChain](https://www.langchain.com/)** — LLM orchestration (chains, retrievers, prompts)
- **[LangChain Groq](https://python.langchain.com/docs/integrations/chat/groq/)** — LLM inference via Groq API (`openai/gpt-oss-120b`)
- **[ChromaDB](https://www.trychroma.com/)** — Persistent local vector database
- **[HuggingFace Sentence Transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)** — Text embeddings (`all-MiniLM-L6-v2`)
- **[PyPDF](https://pypdf.readthedocs.io/)** — PDF parsing and text extraction
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation and settings management
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server

---

## Project Structure

```
DocuMind/
├── backend/
│   └── app/
│       ├── main.py                  # FastAPI app entry point & router registration
│       ├── config.py                # Settings (API keys, paths) via pydantic-settings
│       ├── api/
│       │   └── routes/
│       │       ├── documents.py     # POST /documents/upload
│       │       ├── chat.py          # POST /chats/chat
│       │       ├── notes.py         # POST /notes/{document_id}
│       │       ├── topics.py        # POST /topics/{document_id}
│       │       ├── quiz.py          # POST /quiz/
│       │       └── flashcards.py    # POST /flashcards/
│       ├── services/
│       │   ├── document_services.py # PDF ingestion, chunking, embedding trigger
│       │   ├── chunk_service.py     # RecursiveCharacterTextSplitter (1000 / 200 overlap)
│       │   ├── embedding_services.py# HuggingFace embeddings + ChromaDB CRUD
│       │   ├── rag_services.py      # History-aware conversational RAG chain
│       │   ├── notes_service.py     # Map-reduce summarization chain
│       │   ├── topic_service.py     # LLM-based topic extraction (JSON output)
│       │   ├── flashcard_service.py # Structured flashcard generation
│       │   └── quiz_service.py      # Structured MCQ quiz generation
│       └── schemas/
│           ├── document.py          # DocumentResponse
│           ├── chat.py              # ChatRequest
│           ├── flashcards.py        # FlashCardRequest / FlashCardResponse
│           └── quiz.py              # QuizRequest / QuizResponse / QuestionSchema
├── data/
│   ├── uploads/                     # Uploaded PDF files (named by UUID)
│   └── chroma_db/                   # Persisted ChromaDB vector collections
├── requirements.txt
└── .env
```

---

## API Reference

### Documents

#### `POST /documents/upload`
Upload a PDF document. The file is parsed, split into chunks, and embedded into ChromaDB.

- **Request:** `multipart/form-data` — field `file` (PDF only)
- **Response:**
```json
{
  "document_id": "uuid-string",
  "filename": "example.pdf",
  "file_size": 102400,
  "title": "Document Title",
  "chunks_size": 42,
  "status": "uploaded"
}
```

---

### Chat

#### `POST /chats/chat`
Ask a question about a previously uploaded document. Maintains full conversation history per session.

- **Request Body:**
```json
{
  "session_id": "user-session-id",
  "document_id": "uuid-string",
  "question": "What is the main argument of Chapter 2?"
}
```
- **Response:**
```json
{
  "session_id": "user-session-id",
  "document_id": "uuid-string",
  "question": "What is the main argument of Chapter 2?",
  "answer": "The main argument is..."
}
```

---

### Notes

#### `POST /notes/{document_id}`
Generate structured study notes for an entire document using a map-reduce summarization chain.

- **Response:**
```json
{
  "document_id": "uuid-string",
  "notes": "## Key Concepts\n...",
  "status": "success"
}
```

---

### Topics

#### `POST /topics/{document_id}`
Extract the main topics covered in a document.

- **Response:**
```json
{
  "document_id": "uuid-string",
  "topics": [
    { "name": "Supervised Learning", "description": "Learning from labeled data." }
  ],
  "total_topics": 5,
  "status": "success"
}
```

---

### Quiz

#### `POST /quiz/`
Generate a multiple-choice quiz from the document.

- **Request Body:**
```json
{
  "document_id": "uuid-string",
  "difficulty": "medium",
  "generation_mode": "full_document",
  "topic": null,
  "num_questions": 10
}
```

| Field | Options | Default |
|---|---|---|
| `difficulty` | `easy`, `medium`, `hard` | — |
| `generation_mode` | `full_document`, `topic` | `full_document` |
| `topic` | any string | `null` |
| `num_questions` | 1–30 | `10` |

- **Response:**
```json
{
  "questions": [
    {
      "question": "What is...?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "B",
      "topic": "Neural Networks"
    }
  ]
}
```

---

### Flashcards

#### `POST /flashcards/`
Generate Q&A flashcards from the document or a specific topic.

- **Request Body:**
```json
{
  "document_id": "uuid-string",
  "generation_mode": "topic",
  "topic": "Gradient Descent",
  "num_flashcards": 10
}
```

| Field | Options | Default |
|---|---|---|
| `generation_mode` | `full_document`, `topic` | `full_document` |
| `topic` | any string | `null` |
| `num_flashcards` | any integer | — |

- **Response:**
```json
{
  "questions": [
    {
      "question": "What is gradient descent?",
      "answer": "An optimization algorithm...",
      "topic": "Gradient Descent"
    }
  ]
}
```

---

## Architecture Overview

```
PDF Upload
    │
    ▼
PyPDF (text extraction per page)
    │
    ▼
RecursiveCharacterTextSplitter
(chunk_size=1000, overlap=200)
    │
    ▼
HuggingFace Embeddings
(all-MiniLM-L6-v2)
    │
    ▼
ChromaDB (persisted collection per document_id)
    │
    ├──► RAG Chain (chat)
    │        └─ history-aware retriever → ChatGroq LLM
    │
    ├──► Map-Reduce Chain (notes)
    │        └─ summarize per chunk → combine → ChatGroq LLM
    │
    ├──► Topic Extraction
    │        └─ full content → ChatGroq LLM → JSON topics
    │
    ├──► Flashcard Generator
    │        └─ full doc or similarity search → structured output
    │
    └──► Quiz Generator
             └─ full doc or similarity search → structured MCQ output
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/)
- A [HuggingFace token](https://huggingface.co/settings/tokens) (for embedding model download)

### Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd DocuMind

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

> **Warning:** Never commit your `.env` file. It is already listed in `.gitignore`.

### Running the Backend

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`

---

## Data Persistence

| Location | Contents |
|---|---|
| `data/uploads/` | Uploaded PDFs, stored as `<document_id>.pdf` |
| `data/chroma_db/` | ChromaDB vector collections, one per document (`document_<id>`) |
| In-memory | Chat history per session (resets on server restart) |

---

## RAG Pipeline Details

The conversational Q&A uses a two-stage chain:

1. **History-Aware Retriever** — Reformulates the user question using past chat history into a standalone query before hitting the vector store.
2. **Stuff Documents Chain** — Injects retrieved chunks into a concise QA prompt and invokes the LLM.

Both stages are wrapped in `RunnableWithMessageHistory` to maintain per-session conversation state.

The Notes service uses a **map-reduce** pattern: the LLM first summarizes each chunk independently (map), then synthesises all summaries into a single set of structured study notes (reduce).
