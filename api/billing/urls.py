from __future__ import annotations

from api.billing.views import router

urlpatterns = [
    *router.urls,
]
