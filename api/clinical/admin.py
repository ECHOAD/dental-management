from __future__ import annotations

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.clinical.models import ClinicalModel


@admin.register(ClinicalModel)
class ClinicalAdmin(ModelAdmin):
    pass
