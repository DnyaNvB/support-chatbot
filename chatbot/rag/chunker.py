from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ".", "؟", "!", "،", " "],
    )

    chunks = []
    for page in pages:
        docs = splitter.create_documents(
            [page["content"]],
            metadatas=[{"url": page["url"]}],
        )
        chunks.extend(docs)
    return chunks