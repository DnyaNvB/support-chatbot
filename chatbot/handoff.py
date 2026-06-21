HANDOFF_KEYWORDS = [
    "شکایت",
    "عصبانی",
    "پشتیبان انسانی",
    "اپراتور",
    "مشکل حل نشد",
    "اشتباه",
    "پولم گم شده",
    "برداشت انجام نشده",
]


def should_handoff(message: str, docs: list) -> bool:
    if any(keyword in message for keyword in HANDOFF_KEYWORDS):
        return True

    if not docs:
        return True

    return False