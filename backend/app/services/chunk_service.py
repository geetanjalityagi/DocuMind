from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(documents):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 250)
    chunks = text_splitter.split_documents(documents)

    return chunks