from decimal import Decimal

from django.db import transaction

from apps.inventory.models import InventoryMovement


@transaction.atomic
def create_inventory_movement(*, product, movement_type, quantity, reason=""):
    quantity = Decimal(quantity)

    if quantity == 0:
        raise ValueError("A quantidade deve ser diferente de zero.")

    current_stock = product.stock_quantity

    if movement_type == InventoryMovement.MovementType.IN:
        new_stock = current_stock + quantity

    elif movement_type == InventoryMovement.MovementType.OUT:
        new_stock = current_stock - quantity

    elif movement_type == InventoryMovement.MovementType.ADJUSTMENT:
        new_stock = current_stock + quantity

    else:
        raise ValueError("Tipo de movimentação inválido.")

    if new_stock < 0:
        raise ValueError("O estoque não pode ser negativo.")

    product.stock_quantity = new_stock
    product.save(update_fields=["stock_quantity", "updated_at"])

    return InventoryMovement.objects.create(
        product=product,
        movement_type=movement_type,
        quantity=quantity,
        balance_after=new_stock,
        reason=reason,
    )
