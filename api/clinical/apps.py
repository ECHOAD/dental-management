from __future__ import annotations

from django.apps import AppConfig


class ClinicalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.clinical"


    def ready(self):
        # Import signals to ensure they are registered
        import api.clinical.signals