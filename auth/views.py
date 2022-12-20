from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, generics, filters

from auth.serializers import *

class AuthViewSet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        try:
            return Token.objects.select_related('user').filter(user=user)
        except:
            Response(status=status.HTTP_404_NOT_FOUND)
            
    def get(self, request, format=None):
        token = self.get_object(request.user)
        if len(token) == 0:
            Token.objects.create(user=request.user)
            serializer = TokenSerializer(self.get_object(request.user), many=True)
            return Response(serializer.data)
        serializer = TokenSerializer(token, many=True)
        return Response(serializer.data)
    
    def delete(self, request, format=None):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_201_CREATED)
   
class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset
    serializer_class = UserSerializer
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]