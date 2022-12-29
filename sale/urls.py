from django.urls import path, include
from sale.views import *

app_name = 'sale'

urlpatterns = [
    path('print/sale/<int:id>/', printPDF),
]