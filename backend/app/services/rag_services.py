import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


groq_api_key = os.getenv("GROP_API_KEY")

def rag_pipeline(seesion_id, file):
    
    llm = ChatGroq(api_key=groq_api_key, model="openai/gpt-oss-120b")






    