from __future__ import annotations

from api import __version__
from api.config.application import PROJECT_VERBOSE_NAME

SPECTACULAR_SETTINGS = {
    "TITLE": PROJECT_VERBOSE_NAME,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "COMPONENT_SPLIT_REQUEST": True,
    "VERSION": __version__,
    "SORT_OPERATIONS": True,  # También tenía un espacio extra antes
    "EXTENSIONS": {  # ✅ corregido
        "rest_framework.filters.OrderingFilter": "api.common.schema_extensions.CustomOrderingFilterExtension",
    },
}