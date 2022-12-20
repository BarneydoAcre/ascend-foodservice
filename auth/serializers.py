from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'last_login',
        ]

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True,)
    class Meta:
        model = Token
        fields = ['user', 'key']
     