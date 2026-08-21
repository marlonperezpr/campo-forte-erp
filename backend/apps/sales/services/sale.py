from django.db import transaction

from apps.inventory.models import InventoryMovement
from apps.inventory.services.inventory import create_inventory_movement


@transaction.atomic
def confirm_sale(sale):
    if sale.status == sale.Status.CONFIRMED:
        raise ValueError("A venda já está confirmada.")

    if not sale.items.exists():
        raise ValueError("Não é possível confirmar uma venda sem itens.")

    items = sale.items.select_related("product")

    for item in items:
        item.full_clean()

        if item.quantity > item.product.stock_quantity:
            raise ValueError(
                f"Estoque insuficiente para o produto: {item.product.name}."
            )

    sale.recalculate_total()

    for item in items:
        create_inventory_movement(
            product=item.product,
            movement_type=InventoryMovement.MovementType.OUT,
            source=InventoryMovement.Source.SALE,
            quantity=item.quantity,
        )

    sale.status = sale.Status.CONFIRMED
    sale.save(update_fields=["status"])
