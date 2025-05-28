from __future__ import annotations

from django.db import models

from api.common.models import BaseModel
from api.config import settings


class ClinicalConfig(models.Model):
    """
    Configuration model for the clinical application.
    This can be used to store settings related to clinical operations.
    """
    name = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Clinical Configuration"
        verbose_name_plural = "Clinical Configurations"


class Patient(BaseModel):
    full_name = models.CharField(max_length=255)
    document_id = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    clinical_history = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Procedure(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    supplies = models.ManyToManyField(
        "inventory.InventoryItem",
        through="ProcedureSupply",
        related_name="used_in_procedures",
    )

    def __str__(self):
        return self.name


class ProcedureSupply(models.Model):
    procedure = models.ForeignKey("clinical.Procedure", on_delete=models.CASCADE, related_name="default_supplies")
    supply = models.ForeignKey("inventory.InventoryItem", on_delete=models.CASCADE, related_name="supply_defaults")
    quantity_required = models.PositiveIntegerField()

    class Meta:
        unique_together = ("procedure", "supply")

    def __str__(self):
        return f"{self.supply.name} x{self.quantity_required} for {self.procedure.name}"


class TreatmentUsedSupply(models.Model):
    treatment = models.ForeignKey("clinical.TreatmentRecord", on_delete=models.CASCADE, related_name="used_supplies")
    supply = models.ForeignKey("inventory.InventoryItem", on_delete=models.CASCADE)
    quantity_used = models.PositiveIntegerField()

    class Meta:
        unique_together = ("treatment", "supply")

    def __str__(self):
        return f"{self.supply.name} x{self.quantity_used} for {self.treatment}"


class TreatmentRecord(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatments")
    procedure = models.ForeignKey("clinical.Procedure", on_delete=models.CASCADE, related_name="treatments")
    dentist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clinical_notes = models.TextField(blank=True)
    invoice = models.ForeignKey("billing.Invoice", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.procedure.name} - {self.patient.full_name} - {self.created_at.strftime('%Y-%m-%d')}"
