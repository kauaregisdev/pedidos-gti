from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from orders.models import Order
from orders.serializers import OrderSerializer
from .models import Business

class BusinessSerializer(serializers.ModelSerializer):
    completed_orders = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = ['name', 'description', 'email', 'phone', 'founded_at', 'completed_orders']

    def get_completed_orders(self, obj):
        request = self.context.get('request')
        orders = Order.objects.filter(status=Order.Status.COMPLETED)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        try:
            paginated = paginator.paginate_queryset(orders, request)
        except NotFound:
            return {
                'count': orders.count(),
                'next': None,
                'previous': None,
                'results': [],
                'detail': 'Página inválida.'
            }

        return {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': OrderSerializer(paginated, many=True).data,
        }
