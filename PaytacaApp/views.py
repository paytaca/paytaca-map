from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Location, Logo
from .serializers import LocationSerializer, LogoSerializer

class LocationListAPIView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class LogoListAPIView(APIView):
    def get(self, request):
        logos = Logo.objects.all()
        serializer = LogoSerializer(logos, many=True)
        return Response(serializer.data)
