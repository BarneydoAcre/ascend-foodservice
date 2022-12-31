from django.urls import path, include
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('sales/', sales_per_month),
]