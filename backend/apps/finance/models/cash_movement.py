from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import BaseModel
from apps.finance.models.cash_register import CashRegister


class CashMovement(BaseModel):

    class MovementType(models.TextChoices):
        IN = "IN", "Entrada"
        OUT = "OUT", "Saída"

    class Source(models.TextChoices):
        SALE = "SALE", "Venda"
        PURCHASE = "PURCHASE", "Compra"
        ADJUSTMENT = "ADJUSTMENT", "Ajuste"
        OTHER = "OTHER", "Outro"

    cash_register = models.ForeignKey(
        CashRegister,
        on_delete=models.PROTECT,
        related_name="movements",
        verbose_name="Caixa",
    )

    movement_type = models.CharField(
        max_length=10,
        choices=MovementType.choices,
        verbose_name="Tipo de movimento",
    )

    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER,
        verbose_name="Origem",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Valor",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Descrição",
    )

    class Meta:
        verbose_name = "Movimentação de Caixa"
        verbose_name_plural = "Movimentações de Caixa"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_movement_type_display()} - " f"R$ {self.amount}"
