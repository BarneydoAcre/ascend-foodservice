from rest_framework import serializers
from . import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partner
        fields = '__all__'