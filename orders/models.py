import uuid
from django.db import models
from django.conf import settings

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        COMPLETED = 'completed', 'Concluído'

    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Cliente'
    )
    total = models.DecimalField('Preço total', max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        'Status do pedido',
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField('Data de criação', auto_now_add=True)
    updated_at = models.DateTimeField('Data de atualização', auto_now=True)

    def __str__(self):
        return f'Pedido {self.id} - {self.user.name}'

    def calculate_total(self):
        self.total = sum(item.subtotal() for item in self.items.all())
        Order.objects.filter(pk=self.pk).update(total=self.total)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class OrderItem(models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Pedido'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Produto'
    )
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    unit_price = models.DecimalField('Preço unitário', max_digits=10, decimal_places=2)

    def subtotal(self):
        if self.unit_price is None:
            return 0
        return self.unit_price * self.quantity

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
