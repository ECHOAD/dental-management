from __future__ import annotations

from django.db import models

from api.common.models import BaseModel


class InventoryItem(BaseModel):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)  # e.g., units, ml, grams
    expiration_date = models.DateField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock_threshold = models.PositiveIntegerField(default=5)


    def __str__(self):
        return self.name