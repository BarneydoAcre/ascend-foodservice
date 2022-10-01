from django.urls import path, include
from . import views

app_name = 'foodservice'

urlpatterns = [
    path('addSale/', views.addSale),
    path('addSaleItems/', views.addSaleItems),
    path('print/<int:id>/', views.printPDF),
]