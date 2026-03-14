from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    texts = []
    metadatas = []

    for doc in docs:

        chunks = splitter.split_text(doc["content"])

        for chunk in chunks:

            texts.append(chunk)

            metadatas.append({
                "source": doc["source"],
                "folder": doc["folder"]
            })

    return texts, metadatas