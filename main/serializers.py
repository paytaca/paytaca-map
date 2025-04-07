from rest_framework import serializers
from .models import Merchant

class MerchantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        exclude = [
            'test_shop',
            'watchtower_merchant_id'
        ]
