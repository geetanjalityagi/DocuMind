import json

from app.config import settings
from langchain_groq import ChatGroq
from app.services.embedding_services import get_vector_store

def extract_topics(document_id: str)->list[dict]:

    llm = ChatGroq(api_key=settings.groq_api_key, model="openai/gpt-oss-120b")

    vectors = get_vector_store(document_id)

    documents = vectors.get()["documents"]

    if not documents:
        raise ValueError("No content found for this document.")

    content = "\n\n".join(documents)

    prompt = f"""
    Extract the main topics from this document.

    Return only valid JSON in this format:
    {{
        "topics": [
            {{
                "name": "Supervised Learning",
                "description": "Learning from labeled data."
            }}
        ]
    }}

    Document:
    {content}
    """

    response = llm.invoke(prompt).content
    result = json.loads(response)

    return result["topics"]