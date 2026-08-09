from django.db import models

from apps.core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nome")

    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço de venda"
    )

    active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["name"]

    stock_quantity = models.DecimalField(
        max_digits=10, decimal_places=3, default=0, verbose_name="Quantidade em estoque"
    )

    def __str__(self):
        return self.name
