from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel
from apps.purchases.models.purchase import Purchase
from apps.accounts.models.product import Product


class PurchaseItem(BaseModel):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, related_name="items", verbose_name="Compra"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_items",
        verbose_name="Produto",
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0.001)],
        verbose_name="Quantidade",
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Custo unitário",
    )

    total_cost = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Custo total"
    )

    def save(self, *args, **kwargs):
        if self.purchase.status == Purchase.Status.CONFIRMED:
            raise ValueError("Itens de uma compra confirmada não podem ser alterados.")
        self.total_cost = self.quantity * self.unit_cost

        super().save(*args, **kwargs)

    def recalculate_total_cost(self):
        pass

    class Meta:
        verbose_name = "Item de Compra"
        verbose_name_plural = "Itens de Compra"

    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"
