import uuid
from django.db import models

class Product(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Nome do produto", max_length=150)
    price = models.DecimalField("Preço do produto", max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price:.2f}'

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
