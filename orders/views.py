from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusSerializer

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'update_status':
            return OrderStatusSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action == 'update_status':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        if instance.status == Order.Status.COMPLETED:
            raise PermissionDenied('Pedidos concluídos não podem ser excluídos.')
        instance.delete()

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
