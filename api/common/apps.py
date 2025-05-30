from django.apps.config import AppConfig


class CommonConfig(AppConfig):
    name = "api.common"

    def ready(self):
        import api.clinical.signals  # noqa: F401
        # Register OpenAPI schema extensions
        import api.common.schema_extension

