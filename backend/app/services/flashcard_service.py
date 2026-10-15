from app.config import settings

from langchain_groq import ChatGroq
from app.services.embedding_services import get_vector_store
from app.schemas.flashcards import FlashCardResponse

def generate_flashcards(document_id : str, generation_mode : str, topic : str | None,  num_flashcards: int = int)-> dict:

    llm = ChatGroq(api_key=settings.groq_api_key, model="openai/gpt-oss-120b")

    vectors = get_vector_store(document_id)

    if generation_mode == "full_document":
        documents = vectors.get()["documents"]
        content = "\n\n".join((doc for doc in documents if doc))

    elif generation_mode == "topic":
        if not topic:
            raise ValueError("Topic is required.")

        documents = vectors.similarity_search(topic.strip(), k=4)
        content = "\n\n".join(doc.page_content for doc in documents if doc.page_content)

    else:
        raise ValueError("Invalid generation mode.")

    if not content.strip():
        raise ValueError("No document content found.")

    
    prompt = f"""
    You are StudyMind, an expert educational flashcard generator.

    Generate exactly {num_flashcards} high-quality flashcards using
    ONLY the document content provided below.

    Generation mode: {generation_mode}
    Selected topic: {
        topic.strip() if generation_mode == "topic" and topic
        else "Entire document" if generation_mode == "full_document"
        else "Not specified"
    }

    Requirements:

    1. Generate exactly {num_flashcards} flashcards.
    2. Each flashcard must contain:
    - question: A clear, concise question testing one concept.
    - answer: An accurate, informative, easy-to-revise answer.
    3. If generation_mode is "full_document":
    - Cover important concepts across the entire document.
    - Prioritize definitions, key facts, formulas, processes,
        relationships, differences, and important examples.
    4. If generation_mode is "topic":
    - Focus exclusively on the selected topic.
    - Avoid unrelated concepts unless needed for context.
    5. Use ONLY information supported by the supplied content.
    Never invent facts or introduce unsupported information.
    6. Avoid duplicate, repetitive, or nearly identical questions.
    7. Test understanding and recall rather than copying sentences
    directly from the document.
    8. Keep answers concise but sufficiently informative.
    9. Each question must have one clear, relevant answer.
    10. Vary the question styles where appropriate, such as:
        - What is ...?
        - Why is ... important?
        - How does ... work?
        - What is the difference between ... and ...?
        - What are the main steps of ...?
    11. Do not generate multiple-choice options or MCQs.
    12. Return output matching the required FlashCardResponse schema.
    13. Return structured data only, without Markdown fences,
        introductions, or additional commentary.

    DOCUMENT CONTENT:
    {content}
    """

    structured = llm.with_structured_output(FlashCardResponse)
    answer = structured.invoke(prompt)

    return answer.model_dump()
