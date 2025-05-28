from __future__ import annotations

from rest_framework import serializers
from api.clinical.models import ClinicalConfig, Patient, ProcedureSupply, Procedure
from api.inventory.models import InventoryItem


class ClinicalConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalConfig
        exclude = ("id",)

    def to_representation(self, instance):
        return {config.name: config.value for config in instance}


class PatientSerializer(serializers.Serializer):
    last_visit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'document_id', 'phone', 'email', 'address', 'clinical_history', 'last_visit']

    def get_last_visit(self, obj):
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

    class Meta:
        model = ProcedureSupply
        fields = ["id", "supply", "supply_id", "quantity_required"]


class ProcedureSerializer(serializers.ModelSerializer):
    default_supplies = ProcedureSupplySerializer(
        many=True, source="default_supplies", required=False
    )

    class Meta:
        model = Procedure
        fields = ["id", "name", "price", "description", "default_supplies"]

    def create(self, validated_data):
        supplies_data = validated_data.pop("default_supplies", [])
        procedure = Procedure.objects.create(**validated_data)

        for supply_data in supplies_data:
            ProcedureSupply.objects.create(procedure=procedure, **supply_data)

        return procedure

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