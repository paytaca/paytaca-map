from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Location
from .serializers import LocationSerializer

class LocationListAPIView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
