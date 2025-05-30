from __future__ import annotations

from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from api.clinical.models import ClinicalConfig, Patient, ProcedureSupply, Procedure, DentistAssistant
from api.inventory.models import InventoryItem
from api.user.models import User
from api.user.serializers import UserSerializer


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
        fields = ["id", "name", "price", "description"]  # Sin default_supplies

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