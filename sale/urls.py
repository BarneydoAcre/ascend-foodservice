from django.urls import path, include
from sale.views import *

app_name = 'foodservice'

urlpatterns = [
    # path('sale/', SaleViewSet.as_view()),
    # path('addSale/', views.addSale),
    # path('addSaleItems/', views.addSaleItems),
    # path('getSale/', views.getSale),
    # path('getSaleItems/', views.getSaleItems),
    # path('deleteSale/', views.deleteSale),
    path('print/<int:id>/', printPDF),
]