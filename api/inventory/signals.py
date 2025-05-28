from django.db.models.signals import post_save
from django.dispatch import receiver
from api.inventory.models import InventoryItem
from api.notification.models import Notification

@receiver(post_save, sender=InventoryItem)
def handle_inventory_stock_change(sender, instance, **kwargs):
    item_name = instance.name
    threshold = instance.stock_threshold

    if instance.quantity <= threshold:
        Notification.objects.get_or_create(
            title=f"Low stock: {item_name}",
            message=f"The item '{item_name}' has {instance.quantity} unit(s) left.",
            type="inventory",
        )
    else:
        Notification.objects.filter(
            type="inventory",
            title=f"Low stock: {item_name}",
        ).delete()