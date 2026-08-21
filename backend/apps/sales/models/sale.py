from django.db import models
from django.db.models import Sum
from apps.accounts.models import Customer
from apps.core.models import BaseModel


class Sale(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Rascunho"
        CONFIRMED = "CONFIRMED", "Confirmado"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sales",
        verbose_name="Cliente",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Status",
    )

    sale_date = models.DateField(verbose_name="Data da Venda")

    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Valor Total"
    )

    def recalculate_total(self):
        self.total_amount = self.items.aggregate(total=Sum("total_price"))["total"] or 0
        self.save(update_fields=["total_amount"])

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ["-sale_date", "-created_at"]

    def __str__(self):
        return f"Venda #{self.pk}"
