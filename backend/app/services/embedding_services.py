from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def embed_text(chunks):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = HuggingFaceEmbeddings(model_name=model)

    vectors = Chroma.from_documents(documents=chunks, embedding=embeddings)
    retriever = vectors.as_retriever()

    return retriever

