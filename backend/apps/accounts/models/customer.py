from django.db import models
from apps.core.models import BaseModel


class Customer(BaseModel):
    name = models.CharField(max_length=150, verbose_name="Nome")

    cpf_cnpj = models.CharField(max_length=18, blank=True, verbose_name="CPF/CNPJ")

    phone = models.CharField(max_length=20, verbose_name="Telefone")

    email = models.EmailField(blank=True, verbose_name="E-mail")

    adress = models.TextField(blank=True, verbose_name="Endereço")

    notes = models.BooleanField(default=True, verbose_name="Observações")

    active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name
