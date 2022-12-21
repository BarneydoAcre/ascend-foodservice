from rest_framework import serializers
from sale.models import *

class SaleItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItems
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    sale_items = SaleItemsSerializer(read_only=True)
    class Meta:
        model = Sale
        fields = [
            'id',
            'company',
            'company_worker',
            'value',
            'delivery',
            'canceled',
            'total',
            'sale_items'
        ]