from datetime import datetime, timedelta, timezone


def now():
    """
    Custom time.now() function required by the assignment.
    """
    return datetime.now(timezone.utc)


def extract_processing_hours(docs) -> float:
    """
    Estimate processing duration from retrieved RAG documents.

    Requirement:
    Remaining Time =
    (transaction_start_time + processing_time_from_RAG)
    - time.now()
    """

    text = "\n".join(
        doc.page_content.lower()
        for doc in docs
    )

    # Instant withdrawals/deposits
    if "چند ثانیه" in text:
        return 0

    # Blockchain confirmations
    if (
        "تایید" in text
        or "confirmation" in text
        or "شبکه" in text
    ):
        return 1

    # Banking cycles
    if (
        "سیکل" in text
        or "بانکی" in text
        or "پایا" in text
    ):
        return 24

    # Fallback
    return 24


def calculate_remaining_time(
    transaction_start_time: str,
    processing_hours: float,
) -> str:
    """
    Calculates:

    Remaining Time =
    (transaction_start_time + processing_time)
    - time.now()
    """

    start = datetime.fromisoformat(
        transaction_start_time.replace(
            "Z",
            "+00:00",
        )
    )

    finish = start + timedelta(
        hours=float(processing_hours)
    )

    remaining = finish - now()

    if remaining.total_seconds() <= 0:
        return "زمان تقریبی پردازش به پایان رسیده است."

    hours = int(
        remaining.total_seconds() // 3600
    )

    minutes = int(
        (remaining.total_seconds() % 3600) // 60
    )

    return (
        f"حدود {hours} ساعت و "
        f"{minutes} دقیقه باقی مانده است."
    )