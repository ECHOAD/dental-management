from __future__ import annotations

from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from api.clinical.models import ClinicalConfig, Patient, ProcedureSupply, Procedure, DentistAssistant, TreatmentRecord, \
    TreatmentUsedSupply
from api.clinical.services.treatment import TreatmentService
from api.inventory.models import InventoryItem
from api.user.models import User
from api.user.serializers import UserSerializer, MinimalUserSerializer
from api.user.utils import get_dentist_from_user


class ClinicalConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalConfig
        exclude = ("id",)

    def to_representation(self, instance):
        return {config.name: config.value for config in instance}


class DentistAssistantSerializer(serializers.ModelSerializer):
    dentist = UserSerializer(read_only=True)
    assistant = UserSerializer(read_only=True)
    dentist_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Dentist'),
        source='dentist',
        write_only=True
    )
    assistant_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Assistant'),
        source='assistant',
        write_only=True
    )

    class Meta:
        model = DentistAssistant
        fields = ('id', 'dentist', 'assistant', 'dentist_id', 'assistant_id', 'created_at')

class PatientSerializer(serializers.ModelSerializer):
    last_visit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'phone', 'email', 'address', 'clinical_history', 'date_of_birth', 'last_visit']

    def get_last_visit(self, obj) -> datetime | None:
        last_treatment = obj.treatments.order_by('-created_at').first()
        if last_treatment:
            return last_treatment.created_at.date()
        return None


class MinimalPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "full_name", "email"]

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ["id", "name"]



class ProcedureSupplySerializer(serializers.ModelSerializer):
    supply = InventoryItemSerializer(read_only=True)
    supply_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), source="supply", write_only=True
    )
    quantity_required = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = ProcedureSupply
        fields = [ "supply", "supply_id", "quantity_required"]


class ProcedureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ["id", "name", "price", "description"]

class MinimalProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ["id", "name", "price"]

class ProcedureDetailSerializer(serializers.ModelSerializer):
    default_supplies = ProcedureSupplySerializer(
        many=True, required=True
    )

    class Meta:
        model = Procedure
        fields = ["id", "name", "price", "description", "default_supplies"]

    @transaction.atomic
    def create(self, validated_data):
        supplies_data = validated_data.pop("default_supplies", [])
        procedure = Procedure.objects.create(**validated_data)

        for supply_data in supplies_data:
            ProcedureSupply.objects.create(procedure=procedure, **supply_data)

        return procedure

    @transaction.atomic
    def update(self, instance, validated_data):
        supplies_data = validated_data.pop("default_supplies", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if supplies_data:
            instance.default_supplies.all().delete()
            for supply_data in supplies_data:
                ProcedureSupply.objects.create(procedure=instance, **supply_data)

        return instance


class TreatmentUsedSupplySerializer(serializers.ModelSerializer):
    supply = InventoryItemSerializer(read_only=True)
    supply_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(),
        source="supply",
        write_only=True
    )

    class Meta:
        model = TreatmentUsedSupply
        fields = ["id", "supply", "supply_id", "quantity_used"]

class TreatmentRecordListSerializer(serializers.ModelSerializer):
    patient = MinimalPatientSerializer(read_only=True)
    dentist = MinimalUserSerializer(read_only=True)
    procedure = MinimalProcedureSerializer(read_only=True)

    class Meta:
        model = TreatmentRecord
        fields = [
            "id",
            "patient",
            "dentist",
            "procedure",
            "clinical_notes",
            "created_at",
        ]


class TreatmentRecordDetailSerializer(serializers.ModelSerializer):
    supplies = TreatmentUsedSupplySerializer(many=True, read_only=True, source="used_supplies")
    patient = MinimalPatientSerializer(read_only=True)
    dentist = MinimalUserSerializer(read_only=True)
    procedure = MinimalProcedureSerializer(read_only=True)

    class Meta:
        model = TreatmentRecord
        fields = [
            "id",
            "dentist",
            "patient",
            "procedure",
            "clinical_notes",
            "supplies",
            "created_at",
        ]

class TreatmentRecordCreateSerializer(serializers.ModelSerializer):
    used_supplies = TreatmentUsedSupplySerializer(many=True, write_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source="patient", write_only=True, required=True)
    procedure_id = serializers.PrimaryKeyRelatedField(queryset=Procedure.objects.all(), source="procedure", write_only=True, required=True)

    class Meta:
        model = TreatmentRecord
        fields = [
            "patient_id",
            "procedure_id",
            "clinical_notes",
            "used_supplies",
        ]

    def validate(self, attrs):
        user = self.context["request"].user
        try:
            attrs["dentist"] = get_dentist_from_user(user)
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})
        return attrs



    def create(self, validated_data):
        used_supplies_data = validated_data.pop("used_supplies", [])
        return TreatmentService.create_treatment_with_invoice_and_inventory(
            validated_data, used_supplies_data
        )


class TreatmentRecordUpdateSerializer(serializers.ModelSerializer):
    used_supplies = TreatmentUsedSupplySerializer(many=True, write_only=True)
    patient = MinimalPatientSerializer(read_only=True)
    dentist = MinimalUserSerializer(read_only=True)
    procedure = MinimalProcedureSerializer(read_only=True)
    clinical_notes = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    class Meta:
        model = TreatmentRecord
        fields = [
            "patient",
            "dentist",
            "procedure",
            "clinical_notes",
            "used_supplies",
        ]

    def update(self, instance, validated_data):
        used_supplies_data = validated_data.pop("used_supplies", [])
        instance.clinical_notes = validated_data.get("clinical_notes", instance.clinical_notes)
        instance.save()

        # Update or create used supplies
        for supply_data in used_supplies_data:
            supply_id = supply_data.get("supply_id")
            quantity_used = supply_data.get("quantity_used")
            if supply_id and quantity_used is not None:
                TreatmentUsedSupply.objects.update_or_create(
                    treatment=instance,
                    supply_id=supply_id,
                    defaults={"quantity_used": quantity_used}
                )

        return instance