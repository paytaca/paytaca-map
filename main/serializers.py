from rest_framework import serializers
from .models import Merchant, Category

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
