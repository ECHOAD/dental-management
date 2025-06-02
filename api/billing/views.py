from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from rest_framework import status as drf_status

from django_filters.rest_framework import DjangoFilterBackend

from api.billing.serializers import InvoiceStatusUpdateSerializer
from api.common.pagination import CustomPageNumberPagination
from api.common.routers import CustomViewRouter
from api.billing import serializers
from api.user.utils import get_queryset_for_user
from api.common.permissions import IsInGroup


if TYPE_CHECKING:
    from rest_framework.request import Request

router = CustomViewRouter()


@router.register(r"invoices", name="invoices", basename="invoices")
class InvoiceView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = serializers.InvoiceSerializer
    required_groups = ["Admin", "Dentist", "Assistant"]
    permission_classes = [IsAuthenticated, IsInGroup]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["treatment_record__patient__id", "treatment_record__dentist__id"]
    pagination_class = CustomPageNumberPagination


    def get_queryset(self):
        return get_queryset_for_user(self.request.user, "billing.Invoice", "treatment_record__dentist")

    @action(detail=True, methods=["patch"], url_path="update-status", url_name="update_status")
    def update_status(self, request, pk=None):
        invoice = self.get_object()
        serializer = InvoiceStatusUpdateSerializer(invoice, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "update_status":
            return serializers.InvoiceStatusUpdateSerializer
        return super().get_serializer_class()