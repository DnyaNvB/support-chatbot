import time
import uuid

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

from chatbot.serializers import ChatRequestSerializer
from chatbot.safety.guardrails import is_prompt_injection
from chatbot.handoff import should_handoff
from chatbot.tools.time_tool import (
    calculate_remaining_time,
    extract_processing_hours,
)
from chatbot.models import ChatLog
from chatbot.rag.retriever import retrieve_context
from chatbot.rag.generator import generate_answer


class ChatAPIView(APIView):
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        transaction_start_time = serializer.validated_data.get(
            "transaction_start_time"
        )

        if is_prompt_injection(message):
            answer = "درخواست شما قابل پردازش نیست."

            ChatLog.objects.create(
                user_message=message,
                answer=answer,
                retrieved_sources=[],
                handoff=False,
            )

            return Response({
                "answer": answer,
                "handoff": False,
                "sources": [],
            })

        docs = retrieve_context(message)
        handoff = should_handoff(message, docs)

        if handoff:
            answer = (
                "برای بررسی دقیق‌تر، این گفتگو باید به پشتیبان انسانی منتقل شود."
            )
            docs = []
        else:
            answer = generate_answer(message, docs)

        if transaction_start_time and docs:
            processing_hours = extract_processing_hours(docs)

            remaining = calculate_remaining_time(
                transaction_start_time,
                processing_hours=processing_hours,
            )

            answer += (
                "\n\n"
                "بر اساس زمان شروع تراکنش و زمان پردازش ذکرشده در مرکز راهنمای تبدیل:\n"
                f"{remaining}"
            )

        sources = list({
            doc.metadata.get("url", "")
            for doc in docs[:3]
            if doc.metadata.get("url")
        })

        ChatLog.objects.create(
            user_message=message,
            answer=answer,
            retrieved_sources=sources,
            handoff=handoff,
        )

        return Response({
            "answer": answer,
            "handoff": handoff,
            "sources": sources,
        })


class DebouncedChatAPIView(APIView):
    DEBOUNCE_SECONDS = 7

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data["message"]
        transaction_start_time = serializer.validated_data.get(
            "transaction_start_time"
        )

        session_id = request.data.get("session_id") or "default-user"

        cache_key_messages = f"debounce_messages:{session_id}"
        cache_key_timestamp = f"debounce_timestamp:{session_id}"

        messages = cache.get(cache_key_messages, [])
        messages.append(message)

        current_timestamp = str(uuid.uuid4())

        cache.set(cache_key_messages, messages, timeout=30)
        cache.set(cache_key_timestamp, current_timestamp, timeout=30)

        time.sleep(self.DEBOUNCE_SECONDS)

        latest_timestamp = cache.get(cache_key_timestamp)

        if latest_timestamp != current_timestamp:
            return Response({
                "status": "queued",
                "answer": "",
                "handoff": False,
                "sources": [],
            })

        final_messages = cache.get(cache_key_messages, [])

        greetings = {"سلام", "درود", "hello", "hi"}

        important_messages = [
            msg for msg in final_messages
            if msg.strip().lower() not in greetings
        ]

        combined_message = (
            important_messages[-1]
            if important_messages
            else final_messages[-1]
        )

        cache.delete(cache_key_messages)
        cache.delete(cache_key_timestamp)

        fake_request_data = {
            "message": combined_message
        }

        if transaction_start_time:
            fake_request_data["transaction_start_time"] = transaction_start_time

        request._full_data = fake_request_data

        return ChatAPIView().post(request)