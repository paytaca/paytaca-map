from rest_framework import serializers
from .models import  Merchants, Location, Category, Logo

class MerchantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchants
        fields = '__all__'
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = '__all__'
