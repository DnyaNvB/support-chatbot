from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
    transaction_start_time = serializers.CharField(
        required=False,
        allow_blank=True
    )