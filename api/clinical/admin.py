from __future__ import annotations

from django.contrib import admin

from api.clinical.models import (
    ClinicalConfig,
    Patient,
    Procedure,
    TreatmentRecord, ProcedureSupply, TreatmentUsedSupply,
)


@admin.register(ClinicalConfig)
class ClinicalConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "short_value")
    search_fields = ("name",)
    ordering = ("name",)

    def short_value(self, obj):
        return obj.value[:75] + ("..." if len(obj.value) > 75 else "")

    short_value.short_description = "Value Preview"


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "document_id", "phone", "email", "last_visit")
    search_fields = ("full_name", "document_id", "email")
    list_filter = ("created_at",)
    ordering = ("full_name",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Last Visit")
    def last_visit(self, obj):
        return obj.treatments.order_by(
            "-created_at").first().created_at if obj.treatment_records.exists() else "No Visits"


class ProcedureSupplyInline(admin.TabularInline):
    model = ProcedureSupply
    extra = 1
    autocomplete_fields = ["supply"]


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [ProcedureSupplyInline]


class UsedSupplyInline(admin.TabularInline):
    model = TreatmentUsedSupply
    extra = 1
    autocomplete_fields = ["supply"]


@admin.register(TreatmentRecord)
class TreatmentRecordAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "procedure",
        "dentist",
        "created_at",
        "has_invoice",
    )
    search_fields = (
        "patient__full_name",
        "procedure__name",
        "dentist__username",
    )
    list_filter = ("created_at", "procedure__name", "dentist__groups")
    ordering = ("-created_at",)
    autocomplete_fields = ("patient", "procedure", "dentist", "invoice")
    readonly_fields = ("created_at", "updated_at")
    inlines = [UsedSupplyInline]

    def has_invoice(self, obj):
        return bool(obj.invoice)

    has_invoice.boolean = True
    has_invoice.short_description = "Has Invoice"
