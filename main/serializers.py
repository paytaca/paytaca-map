from rest_framework import serializers
from .models import Merchant, Category, FeedPost


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'short_name']


class MerchantsSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Merchant
        exclude = [
            'test_shop',
        ]

    def get_categories(self, obj):
        return CategorySerializer(obj.categories.all(), many=True).data


class FeedPostSerializer(serializers.ModelSerializer):
    merchants = serializers.SerializerMethodField()

    class Meta:
        model = FeedPost
        fields = [
            'id',
            'platform',
            'link',
            'description',
            'posted_at',
            'created_at',
            'merchants',
        ]

    def get_merchants(self, obj):
        return [{'id': merchant.id, 'name': merchant.name} for merchant in obj.merchants.all()]
