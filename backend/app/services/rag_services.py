from app.config import settings

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from app.services.embedding_services import get_vector_store

chat_store = {}

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in chat_store:
        chat_store[session_id] = ChatMessageHistory()
    return chat_store[session_id]

def rag_pipeline(session_id, document_id, input):
    
    llm = ChatGroq(api_key=settings.groq_api_key, model="openai/gpt-oss-120b")

    vector_store = get_vector_store(document_id)

    retriever = vector_store.as_retriever()

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question" "which might reference context in the chat history, " "formulate a standalone question which can be understood " "without the chat history. Do NOT answer the question, " "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_system = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_system)

    # Anser Questions

    system_prompt = ( 
        "You are an assistant for question-answering tasks. " "Use the following pieces of retrieved context to answer " "the question. If you don't know the answer, say that you " "don't know. Use three sentences maximum and keep the " "answer concise." "\n\n" "{context}" 
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )

    stuff_documents = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, stuff_documents)


    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key = "input",
        history_messages_key = "chat_history",
        output_messages_key = "answer"
    )

    response = conversational_rag_chain.invoke(
        {"input" : input},
        config = {
            "configurable" : {"session_id" : session_id}
        }
    )

    return response['answer']