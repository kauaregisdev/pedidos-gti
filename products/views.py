import uuid
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer

class ProductListView(ListAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            uuid.UUID(self.kwargs['pk'])
        except ValueError:
            raise ValidationError({'detail': 'ID inválido.'})

        try:
            return super().get_object()
        except Exception:
            raise NotFound({'detail': 'Não encontrado.'})
