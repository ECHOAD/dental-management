from __future__ import annotations

from rest_framework import serializers


class InventorySerializer(serializers.Serializer):
    message = serializers.CharField()
