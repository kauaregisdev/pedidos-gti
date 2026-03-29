import uuid
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from .models import News
from .serializers import NewsSerializer

class NewsListView(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

class NewsDetailView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
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
