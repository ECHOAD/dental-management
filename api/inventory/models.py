from __future__ import annotations

from django.db import models

from api.common.models import BaseModel


class InventoryItem(BaseModel):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)  # e.g., units, ml, grams
    expiration_date = models.DateField(blank=True, null=True)
    manufacturer = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="N/A"
    )
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock_threshold = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name