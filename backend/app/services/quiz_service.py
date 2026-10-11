from app.config import settings

from langchain_groq import ChatGroq
from app.services.embedding_services import get_vector_store
from app.schemas.quiz import QuizResponse

def generate_quiz(document_id : str, difficulty : str, generation_mode : str, topic : str | None, num_questions : int)-> dict:

    llm = ChatGroq(api_key=settings.groq_api_key, model="openai/gpt-oss-120b")

    vectors = get_vector_store(document_id)

    if difficulty.lower() not in {"easy", "medium", "hard"}:
         raise ValueError("Invalid difficulty level.")

    if not 1 <= num_questions <= 30:
        raise ValueError("Questions must be between 1 and 30.")

    if generation_mode == "full_document":
        documents = vectors.get()["documents"]
        content = "\n\n".join((doc for doc in documents if doc))

    elif generation_mode == "topic":
        if not topic:
            raise ValueError("Topic is required.")

        documents = vectors.similarity_search(topic.strip(), k=4)
        content = "\n\n".join(doc.page_content for doc in documents if doc.page_contentquiz_service)

    else:
        raise ValueError("Invalid generation mode.")

    if not content.strip():
        raise ValueError("No document content found.")

    prompt = f"""
    You are an expert educational quiz generator.

    Generate exactly {num_questions} multiple-choice questions
    using ONLY the document content provided below.

    Difficulty: {difficulty.lower()}
    Generation mode: {generation_mode}
    Selected topic: {topic if generation_mode == "topic" else "Entire document"}

    Requirements:
    1. Generate exactly {num_questions} questions.
    2. Every question must have exactly four answer options.
    3. Options must contain complete answer text.
    4. correct_answer must be A, B, C, or D.
    5. The correct_answer letter must match the corresponding option.
    6. Include the topic for every question.
    7. Match the requested difficulty:
    - easy: definitions and basic understanding
    - medium: conceptual understanding and application
    - hard: deeper reasoning based on the document
    8. Avoid duplicate questions.
    9. Do not use facts that are absent from the supplied content.
    10. Return only data matching the required quiz schema.

    DOCUMENT CONTENT:
    {content}
    """

    structured = llm.with_structured_output(QuizResponse)
    answer = structured.invoke(prompt)

    return answer.model_dump()