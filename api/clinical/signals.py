from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.clinical.models import TreatmentRecord

from django.apps import apps

Invoice = apps.get_model("billing", "Invoice")
Inventory = apps.get_model("inventory", "InventoryItem")


@transaction.atomic
@receiver(post_save, sender=TreatmentRecord)
def create_invoice_for_treatment(sender, instance, created, **kwargs):
    if not created or instance.invoice:
        return

    invoice = Invoice.objects.create(
        patient=instance.patient,
        treatment_record=instance,
        total_amount=instance.procedure.price if instance.procedure.price else 0,
    )

    instance.invoice = invoice
    instance.save()


@transaction.atomic
@receiver(post_save, sender=TreatmentRecord)
def update_inventory_for_treatment(sender, instance, created, **kwargs):
    if not created:
        return

    for supply in instance.used_supplies.all():
        inventory_item = Inventory.objects.get(id=supply.supply.id)
        inventory_item.quantity -= supply.quantity_used
        inventory_item.save()