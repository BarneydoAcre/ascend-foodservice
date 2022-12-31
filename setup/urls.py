from django.contrib import admin
from django.urls import path, include

app_name = 'register'

from rest_framework import routers
import sale.views as sale
import register.views as register

router = routers.DefaultRouter()
router.register('sale', sale.SaleViewSet, basename='sale')
router.register('product', register.ProductViewSet, basename='product')
router.register('brand', register.BrandViewSet, basename='brand')
router.register('measure', register.MeasureViewSet, basename='measure')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('accounts/', include('auth.urls')),
    path('default/', include('default.urls')),
    # path('register/', include('register.urls')),
    # path('api-auth/', include('django.contrib.auth.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    path('', include('sale.urls')),
    path('dashboard/', include('dashboard.urls')),
    # path('auth/signin/', LoginViewSet.as_view()),
    # path('auth/signup/', LoginViewSet.as_view()),
]
