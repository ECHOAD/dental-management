from __future__ import annotations

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.billing.models import BillingModel


@admin.register(BillingModel)
class BillingAdmin(ModelAdmin):
    pass
