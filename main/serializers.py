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
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = FeedPost
        fields = [
            'id',
            'platform',
            'link',
            'image_url',
            'preview_image',
            'description',
            'posted_at',
            'created_at',
            'merchants',
        ]

    def get_merchants(self, obj):
        return [{'id': merchant.id, 'name': merchant.name} for merchant in obj.merchants.all()]

    def get_preview_image(self, obj):
        if obj.image:
            return obj.image.url
        return obj.image_url or None
