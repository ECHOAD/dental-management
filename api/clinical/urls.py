from __future__ import annotations

from api.clinical.views import router

urlpatterns = [
    *router.urls,
]
