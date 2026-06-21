import os
from dotenv import load_dotenv
from openai import OpenAI
from chatbot.rag.prompts import SYSTEM_PROMPT

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    timeout=60,
)

MODEL = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

def generate_answer(question: str, docs: list):
    context = "\n\n".join(
        [doc.page_content[:1200] for doc in docs[:3]]
    )
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
سوال کاربر:
{question}

متن‌های بازیابی شده:
{context}

پاسخ فارسی:
""",
        },
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1,
    )

    return response.choices[0].message.content