from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def get_database():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    return Chroma(
        persist_directory="vectorstore/chroma",
        embedding_function=embeddings,
    )


def retrieve_context(query: str):
    db = get_database()

    if "واریز" in query and (
        "ارز" in query or "رمزارز" in query or "دیجیتال" in query
    ):
        docs = db.similarity_search(
            "واریز ارز دیجیتال به صرافی تبدیل تایید شبکه",
            k=3,
            filter={"url": "https://tabdeal.org/help/cryptocurrency-deposit-guide/"},
        )
        if docs:
            return docs

    if "برداشت" in query and (
        "ارز" in query or "رمزارز" in query or "دیجیتال" in query
    ):
        docs = db.similarity_search(
            "برداشت ارز دیجیتال از صرافی تبدیل",
            k=3,
            filter={"url": "https://tabdeal.org/help/cryptocurrency-withdraw-guide/"},
        )
        if docs:
            return docs

    if "برداشت" in query and "تومان" in query:
        docs = db.similarity_search(
            "برداشت تومان برداشت تومانی سیکل بانکی برداشت آنی",
            k=3,
            filter={"url": "https://tabdeal.org/help/rial-withdraw-guide/"},
        )
        if docs:
            return docs

    if "واریز" in query and "تومان" in query:
        docs = db.similarity_search(
            "واریز تومان روش‌های واریز تومان درگاه پرداخت واریز شناسه‌دار کارت به کارت",
            k=3,
            filter={"url": "https://tabdeal.org/help/rial-deposit-guide/"},
        )
        if docs:
            return docs

    docs = db.similarity_search(query, k=8)
    return docs[:3]