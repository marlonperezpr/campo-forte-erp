from django.core.validators import MinValueValidator
from django.db import models

from apps.accounts.models import Product
from apps.core.models import BaseModel
from apps.sales.models.sale import Sale


class SaleItem(BaseModel):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name="items", verbose_name="Venda"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_item",
        verbose_name="Produto",
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0.001)],
        verbose_name="Quantidade",
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preço Unitário",
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Preço Total",
    )

    def delete(self, *args, **kwargs):
        if self.sale.status == Sale.Status.CONFIRMED:
            raise ValueError("Itens de uma venda confirmada não podem ser excluídos")

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.sale.status == Sale.Status.CONFIRMED:
            raise ValueError("Itens de uma venda confirmada não podem ser alterados")

        self.total_price = self.quantity * self.unit_price

        super().save(*args, **kwargs)
