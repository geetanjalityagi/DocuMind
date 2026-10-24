from app.config import settings
from langchain_groq import ChatGroq

from app.services.embedding_services import get_vector_store


def generate_notes(document_id):

    llm = ChatGroq(api_key=settings.groq_api_key, model="openai/gpt-oss-120b")

    vectors = get_vector_store(document_id)

    raw_documents = vectors.get()["documents"]

    if not raw_documents:
        raise ValueError("No document content found for this document ID.")

    content = "\n\n".join(text for text in raw_documents if text)

    if not content.strip():
        raise ValueError("Document content is empty.")

    prompt = f"""
    You are an expert study notes generator.

    Create detailed, well-organized study notes from the document content below.

    Include:
    - Key concepts and definitions
    - Important facts and data points
    - Main ideas and supporting details
    - Examples where relevant
    - Relationships between concepts

    Format the notes clearly using markdown with:
    - Headers (##) for major sections
    - Bullet points for lists
    - **Bold** for key terms
    - Code blocks if applicable

    DOCUMENT CONTENT:
    {content}
    """

    response = llm.invoke(prompt)

    return response.content
