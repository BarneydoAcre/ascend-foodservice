from rest_framework import serializers
from . import models


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partner
        fields = [
            'id',
            'person_f_j',
            'type_client',
            'type_provider',
            'type_conveyor',
            'name',
            'fantasy',
            'cpf',
            'rg',
            'cnpj',
            'ie',
            'phone_number',
            'email',
            'cep',
            'street',
            'district',
            'city',
            'num',
        ]