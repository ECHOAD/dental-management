from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.clinical.models import ClinicalConfig, Patient, Procedure
from api.clinical.serializers import ClinicalConfigSerializer, PatientSerializer, ProcedureSerializer
from api.common.permissions import IsInGroup
from api.common.routers import CustomViewRouter

if TYPE_CHECKING:
    from rest_framework.request import Request

router = CustomViewRouter()


@router.register(r"clinical/config", name="clinical-config")
class ClinicalConfigViewSet(ModelViewSet):
    queryset = ClinicalConfig.objects.all()
    serializer_class = ClinicalConfigSerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_groups = ["Admin"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


@router.register(r"clinical/patients", name="patients")
class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_groups = ["Admin", "Dentist", "Assistant"]


@router.register(r"clinical/procedures", name="procedures")
class ProcedureViewSet(ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    permission_classes = [IsAuthenticated, IsInGroup]
    required_groups = ["Admin", "Dentist", "Assistant"]

