from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend
from api.common.pagination import CustomPageNumberPagination
from api.common.permissions import IsInGroup

from api.common.routers import CustomViewRouter
from api.inventory import serializers
from api.inventory.models import InventoryItem

if TYPE_CHECKING:
    from rest_framework.request import Request

router = CustomViewRouter()


@router.register(r"inventory", name="inventory", basename="inventory")
class InventoryView(ModelViewSet):
    serializer_class = serializers.InventorySerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "is_active"]
    search_fields = ["name", ]

    def get_permissions(self):
        if self.action in ["retrieve", "list"]:
            self.permission_classes = [IsAuthenticated, IsInGroup]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsInGroup]
        return super().get_permissions()

    def get_required_groups(self):
        if self.action in ["retrieve", "list"]:
            return ["Admin", "Dentist", "Assistant"]
        return ["Admin"]

    def get_queryset(self):
        if self.request.user.groups.filter(name="Admin").exists():
            return InventoryItem.objects.all()
        return InventoryItem.objects.filter(is_active=True)

    pagination_class = CustomPageNumberPagination
