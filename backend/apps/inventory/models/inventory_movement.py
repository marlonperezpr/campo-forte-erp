from django.db import models

from apps.accounts.models import Product
from apps.core.models import BaseModel


class InventoryMovement(BaseModel):

    class MovementType(models.TextChoices):
        IN = "IN", "Entrada"
        OUT = "OUT", "Saída"
        ADJUSTMENT = "ADJUSTMENT", "Ajuste"

    class Source(models.TextChoices):
        PURCHASE = "PURCHASE", "Compra"
        SALE = "SALE", "Venda"
        ADJUSTMENT = "ADJUSTMENT", "Ajuste"
        OTHER = "OTHER", "Outro"

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="inventory_movements",
        verbose_name="Produto",
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
        verbose_name="Tipo de movimento",
    )

    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER,
        verbose_name="Origem",
    )

    quantity = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="Quantidade"
    )

    balance_after = models.DecimalField(
        max_digits=10, decimal_places=3, verbose_name="Saldo após movimentação"
    )

    reason = models.CharField(max_length=255, blank=True, verbose_name="Motivo")

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.product} - "
            f"{self.get_movement_type_display()} - "
            f"{self.quantity}"
        )
