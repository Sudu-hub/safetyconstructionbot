from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_vector_store(texts, metadatas):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    vectorstore.save_local("index_cache/faiss_index")

    return vectorstore


def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        "index_cache/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )