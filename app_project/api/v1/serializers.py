from rest_framework import serializers


class SchulteSerializer(serializers.Serializer):
    """Сериализатор Schulte."""
    username = serializers.CharField(read_only=True)
    record = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)


class StroopSerializer(serializers.Serializer):
    """Сериализатор Stroop."""
    username = serializers.CharField(read_only=True)
    record = serializers.CharField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
