from rest_framework import serializers
from . import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductBrand
        fields = '__all__'

class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductMeasure
        fields = '__all__'
        
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partner
        fields = '__all__'