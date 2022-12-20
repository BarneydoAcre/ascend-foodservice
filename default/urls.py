from django.urls import path, include
from default.views import *

app_name = 'default'

urlpatterns = [
    path('company_worker/', CompanyWorkerViewSet.as_view()),
    # path('auth/register/', views.register),
    # path('getCompany/', views.getCompany),
    # path('getCities/', views.getCities),
    # path('addBugReport/', views.addBugReport),
]