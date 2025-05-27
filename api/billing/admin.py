from __future__ import annotations

from django.contrib import admin

from api.billing.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "total_amount",
        "status",
        "issued_at",
        "paid_at",
        "is_paid",
    )
    search_fields = ("patient__full_name", "id")
    list_filter = ("status", "issued_at", "paid_at")
    ordering = ("-issued_at",)
    readonly_fields = ("patient", "total_amount", "status", "issued_at", "paid_at")

    def is_paid(self, obj):
        return obj.status == "paid"
    is_paid.boolean = True
    is_paid.short_description = "Paid?"

    def has_add_permission(self, request):
        return False  # prevent adding from admin

    def has_delete_permission(self, request, obj=None):
        return False  # prevent deleting from admin