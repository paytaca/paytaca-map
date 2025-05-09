from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Merchant, Category
from .serializers import MerchantsSerializer


class MerchantListView(APIView):
    def get(self, request):
        filter_by_id = request.query_params.get("filter_by_id")
        category_id = request.query_params.get("category_id")
        category_short_name = request.query_params.get("category")
        merchants = Merchant.objects.with_effective_date().filter(test_shop=False)
        if filter_by_id:
            merchant_ids = [int(id) for id in filter_by_id.split(",") if id.isdigit()]
            merchants = merchants.filter(id__in=merchant_ids)
        if category_id:
            merchants = merchants.filter(categories__id=category_id)
        if category_short_name:
            merchants = merchants.filter(categories__short_name=category_short_name)
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
        categories = Category.objects.all()
        return Response([{
            'id': category.id,
            'name': category.name,
            'short_name': category.short_name
        } for category in categories])


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
