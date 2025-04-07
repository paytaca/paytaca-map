from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Merchant
from .serializers import MerchantsSerializer


class MerchantListAPIView(APIView):
    def get(self, request):
        filter_by_id = request.query_params.get("filter_by_id")
        merchants = Merchant.objects.filter(test_shop=False)
        if filter_by_id:
            merchant_ids = [int(id) for id in filter_by_id.split(",") if id.isdigit()]
            merchants = merchants.filter(id__in=merchant_ids)
        serializer = MerchantsSerializer(merchants, many=True)
        return Response(serializer.data)


class LocationListAPIView(APIView):
    def get(self, request):
        merchants = Merchant.objects.filter(test_shop=False)
        locations = [{
            'id': merchant.id,
            'merchant': merchant.id,
            'landmark': merchant.landmark,
            'location': merchant.location,
            'street': merchant.street,
            'town': merchant.town,
            'city': merchant.city,
            'province': merchant.province,
            'state': merchant.state,
            'country': merchant.country,
            'longitude': merchant.longitude,
            'latitude': merchant.latitude
        } for merchant in merchants]
        return Response(locations)


class CategoryListAPIView(APIView):
    def get(self, request):
        merchants = Merchant.objects.filter(test_shop=False)
        categories = [{
            'id': merchant.id,
            'merchant': merchant.id,
            'category': merchant.category
        } for merchant in merchants if merchant.category]
        return Response(categories)


class LogoListAPIView(APIView):
    def get(self, request):
        merchants = Merchant.objects.filter(test_shop=False)
        logos = [{
            'id': merchant.id,
            'merchant': merchant.id,
            'size': merchant.logo_size,
            'url': merchant.logo_url
        } for merchant in merchants if merchant.logo_url]
        return Response(logos)
