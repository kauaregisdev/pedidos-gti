from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from orders.models import Order
from .models import News

@receiver(pre_save, sender=Order)
def store_previous_status(sender, instance, **kwargs):
    if not instance._state.adding:
        try:
            instance._previous_status = Order.objects.get(pk=instance.pk).status
        except Order.DoesNotExist:
            instance._previous_status = None

@receiver(post_save, sender=Order)
def order_news(sender, instance, created, **kwargs):
    if created:
        News.objects.create(
            title='Novo pedido criado',
            description='Um novo pedido foi criado com sucesso.',
        )
        return

    previous_status = getattr(instance, '_previous_status', None)
    if previous_status and previous_status != instance.status:
        status_display = instance.get_status_display()
        News.objects.create(
            title='Status de pedido atualizado',
            description=f'Um pedido foi atualizado para "{status_display}".'
        )

@receiver(post_delete, sender=Order)
def order_deleted_news(sender, instance, **kwargs):
    News.objects.create(
        title='Pedido cancelado',
        description='Um pedido pendente foi cancelado.'
    )
