import json
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chatbot.rag.chunker import chunk_documents


EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
with open("data/tabdeal_help.json", encoding="utf-8") as f:
    pages = json.load(f)
chunks = chunk_documents(pages)
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vectorstore/chroma",
)
print(f"Saved {len(chunks)} chunks to vectorstore/chroma")
