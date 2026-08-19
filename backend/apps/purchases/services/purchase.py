from django.db import transaction

from apps.inventory.services.inventory import create_inventory_movement
from apps.inventory.models import InventoryMovement
from apps.purchases.models.purchase import Purchase


@transaction.atomic
def confirm_purchase(purchase):
    if purchase.status != Purchase.Status.DRAFT:
        raise ValueError("Apenas compras em rascunho podem ser confirmadas.")
    items = purchase.items.all()
    if not items.exists():
        raise ValueError("A compra precisa ter pelo menos um item.")

    for item in items:
        item.full_clean()  # Valida os campos do item de compra

    purchase.recalculate_total()

    for item in items:
        create_inventory_movement(
            product=item.product,
            movement_type=InventoryMovement.MovementType.IN,
            source=InventoryMovement.Source.PURCHASE,
            quantity=item.quantity,
            reason=f"Compra #{purchase.id}",
        )

    purchase.status = Purchase.Status.CONFIRMED
    purchase.save(update_fields=["status"])
