from __future__ import annotations

from rest_framework import serializers


class ClinicalSerializer(serializers.Serializer):
    message = serializers.CharField()
