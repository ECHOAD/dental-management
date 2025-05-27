from __future__ import annotations

from rest_framework import serializers


class BillingSerializer(serializers.Serializer):
    message = serializers.CharField()
