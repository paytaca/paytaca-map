from rest_framework import serializers
from .models import Merchant, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class MerchantsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Merchant
        exclude = [
            'test_shop',
            'watchtower_merchant_id'
        ]
