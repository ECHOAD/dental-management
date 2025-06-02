from api.billing.models import Invoice
from api.inventory.models import InventoryItem
from api.clinical.models import TreatmentRecord, TreatmentUsedSupply, ProcedureSupply

from collections import defaultdict
from typing import Dict, List, Any
from django.db import transaction
from decimal import Decimal


class TreatmentService:
    @staticmethod
    @transaction.atomic
    def create_treatment_with_invoice_and_inventory(data: Dict[str, Any], used_supplies_data: List[Dict[str, Any]]):
        treatment, invoice = TreatmentService._create_treatment_and_invoice(data)

        used_supplies_map = defaultdict(int)
        for item_data in used_supplies_data:
            supply = item_data["supply"]
            quantity = item_data["quantity_used"]
            used_supplies_map[supply.id] += quantity

        TreatmentService._process_default_supplies(treatment, used_supplies_map)
        TreatmentService._process_additional_supplies(treatment, used_supplies_map)

        return treatment

    @staticmethod
    def _create_treatment_and_invoice(data: Dict[str, Any]):
        treatment = TreatmentRecord.objects.create(**data)

        total_amount = Decimal('0')
        if treatment.procedure and treatment.procedure.price:
            total_amount = treatment.procedure.price

        invoice = Invoice.objects.create(
            patient=treatment.patient,
            total_amount=total_amount
        )

        treatment.invoice = invoice
        treatment.save()

        return treatment, invoice

    @staticmethod
    def _process_default_supplies(treatment: TreatmentRecord, used_supplies_map: Dict[int, int]):
        default_supplies = ProcedureSupply.objects.filter(procedure=treatment.procedure)

        for default_supply in default_supplies:
            supply = default_supply.supply
            default_quantity = default_supply.quantity_required
            total_quantity = default_quantity + used_supplies_map.pop(supply.id, 0)

            TreatmentService._create_used_supply(treatment, supply, total_quantity)
            TreatmentService._update_inventory(supply.id, total_quantity)

    @staticmethod
    def _process_additional_supplies(treatment: TreatmentRecord, used_supplies_map: Dict[int, int]):
        for supply_id, quantity in used_supplies_map.items():
            supply = InventoryItem.objects.get(id=supply_id)
            TreatmentService._create_used_supply(treatment, supply, quantity)
            TreatmentService._update_inventory(supply_id, quantity)

    @staticmethod
    def _create_used_supply(treatment: TreatmentRecord, supply: InventoryItem, quantity: int):
        TreatmentUsedSupply.objects.create(
            treatment=treatment,
            supply=supply,
            quantity_used=quantity
        )

    @staticmethod
    def _update_inventory(supply_id: int, quantity: int):
        inventory_item = InventoryItem.objects.select_for_update().get(id=supply_id)
        inventory_item.quantity -= quantity
        inventory_item.save()


    @staticmethod
    @transaction.atomic
    def on_delete_treatment(treatment):

        used_supplies = TreatmentUsedSupply.objects.filter(treatment=treatment)
        for used_supply in used_supplies:
            inventory_item = InventoryItem.objects.select_for_update().get(id=used_supply.supply.id)
            inventory_item.quantity += used_supply.quantity_used
            inventory_item.save()

        used_supplies.delete()
        if treatment.invoice:
            treatment.invoice.delete()

