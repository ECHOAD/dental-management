from __future__ import annotations

from datetime import date

from django.contrib import admin

from api.inventory.models import InventoryItem


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "quantity",
        "unit",
        "expiration_date",
        "is_expired",
        "unit_cost",
    )
    search_fields = ("name",)
    list_filter = ("unit", "expiration_date")
    ordering = ("expiration_date", "name")

    def is_expired(self, obj):
        return obj.expiration_date < date.today()
    is_expired.boolean = True
    is_expired.short_description = "Expired?"