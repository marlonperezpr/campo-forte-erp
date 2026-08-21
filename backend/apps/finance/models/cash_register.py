from decimal import Decimal
from django.db import models
from apps.core.models import BaseModel


class CashRegister(BaseModel):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Aberto"
        CLOSED = "CLOSED", "Fechado"

    opened_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de abertura")
    closed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Data de fechamento"
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Saldo inicial",
    )

    closing_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Saldo de Fechamento",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name="Status",
    )

    class Meta:
        verbose_name = "Caixa"
        verbose_name_plural = "Caixas"
        ordering = ["-opened_at"]

    def __str__(self):
        return f"Caixa #{self.pk} - {self.get_status_display()}"
