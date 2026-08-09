from django.db import models

from apps.core.models import BaseModel
from .product import Product
from .supplier import Supplier


class ProductSupplier(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="product_suppliers",
        verbose_name="Produto",
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="supplier_products",
        verbose_name="Fornecedor",
    )

    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço de compra"
    )

    class Meta:
        verbose_name = "Produto por Fornecedor"
        verbose_name_plural = "Produtos por Fornecedor"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "supplier"],
                name="unique_product_supplier",
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.supplier.name}"
