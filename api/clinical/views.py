from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from api.billing.serializers import InvoiceSerializer
from api.clinical.models import ClinicalConfig, Patient, Procedure
from api.clinical.serializers import ClinicalConfigSerializer, PatientSerializer, ProcedureListSerializer, \
    ProcedureDetailSerializer, TreatmentRecordListSerializer, TreatmentRecordDetailSerializer, \
    TreatmentRecordCreateSerializer, TreatmentRecordUpdateSerializer
from api.common.pagination import CustomPageNumberPagination
from api.common.permissions import IsInGroup
from api.common.routers import CustomViewRouter
from api.user.utils import get_queryset_for_user

if TYPE_CHECKING:
    from rest_framework.request import Request

router = CustomViewRouter()


@router.register(r"clinical/config", name="clinical_config")
class ClinicalConfigViewSet(ModelViewSet):
    queryset = ClinicalConfig.objects.all()
    serializer_class = ClinicalConfigSerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_groups = ["Admin"]
    http_method_names = ['get', 'patch', 'head']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

@router.register(r"clinical/patients", name="patients")
class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.filter(active=True)
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_groups = ["Admin", "Dentist", "Assistant"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = {
        "full_name" : [ "icontains"],
    }
    ordering_fields = ["full_name", "date_of_birth"]
    ordering = ["-created_at"]
    pagination_class = CustomPageNumberPagination




@router.register(r"clinical/procedures", name="procedures")
class ProcedureViewSet(ModelViewSet):
    queryset = Procedure.objects.all()
    required_groups = ["Admin", "Dentist", "Assistant"]
    permission_classes = [IsAuthenticated, IsInGroup]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = {
        "name": ["icontains"],
        "price": ["gte", "lte"],
    }
    ordering_fields = ["name", "price" ]


    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ProcedureListSerializer
        return ProcedureDetailSerializer


@router.register(r"clinical/treatments-records", name="treatments")
class TreatmentRecordViewSet(ModelViewSet):
    required_groups = ["Admin", "Dentist", "Assistant"]
    permission_classes = [IsAuthenticated, IsInGroup]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["patient"]
    search_fields = ["patient__full_name"]

    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TreatmentRecordDetailSerializer
        elif self.action == 'create':
            return TreatmentRecordCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return TreatmentRecordUpdateSerializer
        return TreatmentRecordListSerializer

    def get_queryset(self):
        return get_queryset_for_user(self.request.user, "clinical.TreatmentRecord", "dentist")


    @action(detail=True, methods=['get'], url_path='invoice')
    def invoice(self, request, pk=None):
        treatment = self.get_object()

        invoice = getattr(treatment, "invoice", None)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

