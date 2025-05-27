from __future__ import annotations

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.inventory.models import InventoryModel


@admin.register(InventoryModel)
class InventoryAdmin(ModelAdmin):
    pass
