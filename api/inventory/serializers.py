from __future__ import annotations

from rest_framework import serializers
from api.inventory.models import InventoryItem


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = (
            "id", "name", "unit", "quantity", "unit_cost", "manufacturer" ,"stock_threshold", "expiration_date", "is_active",
        )
        read_only_fields = ("id", "created_at", "updated_at",)
