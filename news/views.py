from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import News
from .serializers import NewsSerializer

class NewsView(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
