from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Business
from .serializers import BusinessSerializer

class BusinessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        business = Business.objects.first()

        if not business:
            return Response(
                {'detail': 'Informações da empresa não disponíveis.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BusinessSerializer(business, context={'request': request})
        return Response(serializer.data)
