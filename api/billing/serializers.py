from __future__ import annotations

from rest_framework import serializers

from api.clinical.serializers import (
    MinimalUserSerializer,
    MinimalPatientSerializer,
)

from api.billing.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    patient = MinimalPatientSerializer(source="treatment_record.patient", read_only=True)
    created_by = MinimalUserSerializer(source="treatment_record.dentist", read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("id", "patient", "created_by", "paid_at", "status")

class InvoiceStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["status"]