from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
    timeout=30,
)

def rewrite_query_for_retrieval(query: str) -> str:
    try:
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "تو یک بازنویس جستجوی فارسی هستی. "
                        "غلط‌های تایپی و محاوره‌ای را اصلاح کن. "
                        "فقط یک عبارت جستجوی کوتاه و رسمی برگردان. "
                        "توضیح نده."
                    ),
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return query