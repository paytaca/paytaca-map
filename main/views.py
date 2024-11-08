from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Merchant, Location, Category, Logo
from .serializers import MerchantsSerializer, LocationSerializer, CategorySerializer, LogoSerializer


class LocationListAPIView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class MerchantListAPIView(APIView):
    def get(self, request):
        filter_by_id = request.query_params.get("filter_by_id")
        merchants = Merchant.objects.filter(test_shop=False)
        if filter_by_id:
            merchant_ids = [int(id) for id in filter_by_id.split(",") if id.isdigit()]
            merchants = merchants.filter(id__in=merchant_ids)
        serializer = MerchantsSerializer(merchants, many=True)
        return Response(serializer.data)
    
class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class LogoListAPIView(APIView):
    def get(self, request):
        logos = Logo.objects.all()
        serializer = LogoSerializer(logos, many=True)
        return Response(serializer.data)
