from app.config import settings
from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.documents import Document

from app.services.embedding_services import get_vector_store


def generate_notes(document_id):

    llm = ChatGroq(api_key=settings.groq_api_key, model="openai/gpt-oss-120b")
   
    vectors = get_vector_store(document_id)

    raw_documents = vectors.get()["documents"]

    documents = [
        Document(page_content=text)
        for text in raw_documents
        if text
    ]

    map_prompt = PromptTemplate(
        template="""
        Summarize the following content.
        Extract the important concepts, definitions, facts,
        and examples.

        Content:
        {text}
        """,
        input_variables=["text"]
    )

    combine_prompt = PromptTemplate(
        template="""
        Create detailed study notes from the following summaries.

        Include:
        - Important concepts
        - Definitions
        - Key points
        - Important facts
        - Examples where useful

        Organize the notes clearly.

        Summaries:
        {text}
        """,
        input_variables=["text"]
    )


    # map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])
    # combine_prompt = PromptTemplate(template=combine_prompt_template, input_variables=["text"])

    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=combine_prompt
    )

    summary = chain.invoke({
        "input_documents":documents
    })

    return summary["output_text"]
