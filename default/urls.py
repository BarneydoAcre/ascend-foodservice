from django.urls import path, include

from . import views

app_name = 'default'

urlpatterns = [
    path('auth/login/', views.login),
    path('auth/register/', views.register),
    path('getCompany/', views.getCompany),
    path('addBugReport/', views.addBugReport),
]