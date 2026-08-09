from django.db import models


class BaseModel(models.Model):
  
  #Modelo base para todos os modelos do projeto, contendo campos comuns como data de criação e atualização.
  
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        abstract = True