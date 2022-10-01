from django.urls import path, include
from . import views

app_name = 'foodservice'

urlpatterns = [
    path('addProduct/', views.addProduct),
    path('getProduct/', views.getProduct),
    path('editProduct/', views.editProduct),
    path('addProductItems/', views.addProductItems),
    path('addProductItem/', views.addProductItem),
    path('getProductItems/', views.getProductItems),
    path('addBrand/', views.addBrand),
    path('getBrand/', views.getBrand),
    path('addMeasure/', views.addMeasure),
    path('getMeasure/', views.getMeasure),
    path('addProductStock/', views.addProductStock),
]