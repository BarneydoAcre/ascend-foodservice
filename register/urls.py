from django.urls import path, include
from . import views

from rest_framework import routers

app_name = 'register'

# router = routers.DefaultRouter() # DefaultRouter(trailing_slash=False)

# urlpatterns = router.urls
urlpatterns = [
    path('addProduct/', views.addProduct),
    path('getProduct/', views.getProduct),
    path('editProduct/', views.editProduct),
    path('deleteProduct/', views.deleteProduct),
    path('deleteProductSale/', views.deleteProductSale),
    path('addProductItems/', views.addProductItems),
    path('addProductItem/', views.addProductItem),
    path('getProductItems/', views.getProductItems),
    path('addBrand/', views.addBrand),
    path('getBrand/', views.getBrand),
    path('addMeasure/', views.addMeasure),
    path('getMeasure/', views.getMeasure),
    path('addProductStock/', views.addProductStock),   
    path('addPartner/', views.addPartner),
    path('getPartner/', views.getPartner),
    path('editPartner/', views.editPartner),
    path('deletePartner/', views.deletePartner),

    # path('', include(router.urls))
]