from django.urls import path, include
from auth.views import *

app_name = 'auth'

urlpatterns = [
    path('auth/', AuthViewSet.as_view()),
]