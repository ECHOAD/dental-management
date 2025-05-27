from __future__ import annotations

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.user.views import router

urlpatterns = [
    *router.urls,
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
