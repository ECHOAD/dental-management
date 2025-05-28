from __future__ import annotations

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.inventory"

def ready() -> None:
    """
    This method is called when the app is ready.
    It can be used to perform any initialization tasks.
    """
    import api.inventory.signals
    # Importing signals to ensure they are registered
    # This is necessary for Django to recognize signal handlers defined in this app