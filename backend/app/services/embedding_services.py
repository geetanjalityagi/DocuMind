from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import CHROMA_DIR

def embed_text(chunks, document_id):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = Chroma(
        collection_name=f"document_{document_id}",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    vector_store.add_documents(chunks)

    return vector_store