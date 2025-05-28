from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.viewsets import ReadOnlyModelViewSet

from api.common.routers import CustomViewRouter
from api.notification.models import Notification
from api.notification.serializers import NotificationSerializer
from rest_framework import permissions


if TYPE_CHECKING:
    from rest_framework.request import Request
    
router = CustomViewRouter()

@router.register(r"notification/", name="notification")
class NotificationViewSet(ReadOnlyModelViewSet):
    queryset = Notification.objects.order_by("-created_at")
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
