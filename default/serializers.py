from rest_framework import serializers

from default.models import *
   
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyWorkerSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = CompanyWorker
        fields = [
            'id',
            'cpf',
            'rg',
            'phone_number',
            'company',
        ]