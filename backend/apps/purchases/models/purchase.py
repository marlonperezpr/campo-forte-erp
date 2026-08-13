from django.db import models

from apps.core.models import BaseModel
from apps.accounts.models.supplier import Supplier

from datetime import date


class Purchase(BaseModel):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Rascunho"
        CONFIRMED = "CONFIRMED", "Confirmada"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Status",
    )

    purchase_date = models.DateField(default=date.today, verbose_name="Data da compra")

    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Valor total"
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="purchases",
        verbose_name="Fornecedor",
    )

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ["-purchase_date"]

    def __str__(self):
        return f"Compra #{self.id} - {self.supplier if self.supplier else 'Sem fornecedor'} - {self.purchase_date} - "
