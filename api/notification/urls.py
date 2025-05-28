from __future__ import annotations

from api.notification.views import router

urlpatterns = [
    *router.urls,
]
