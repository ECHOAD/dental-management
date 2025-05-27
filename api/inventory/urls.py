from __future__ import annotations

from api.inventory.views import router

urlpatterns = [
    *router.urls,
]
