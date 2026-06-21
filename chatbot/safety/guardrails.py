BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "دستورهای قبلی را نادیده بگیر",
    "پرامپت سیستم",
    "نقش خودت را عوض کن",
]


def is_prompt_injection(message: str) -> bool:
    msg = message.lower()
    return any(pattern.lower() in msg for pattern in BLOCKED_PATTERNS)