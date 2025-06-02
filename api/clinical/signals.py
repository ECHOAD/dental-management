from django.db.models.signals import pre_delete
from django.dispatch import receiver

from api.clinical.models import TreatmentRecord
from api.clinical.services.treatment import TreatmentService
from django.apps import apps

Inventory = apps.get_model("inventory", "InventoryItem")


@receiver(pre_delete, sender=TreatmentRecord)
def delete_invoice_with_treatment(sender, instance, **kwargs):
    TreatmentService.on_delete_treatment(instance)

