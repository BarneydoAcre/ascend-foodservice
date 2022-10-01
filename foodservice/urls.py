from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.jwt')),
    # path('', include('suport.urls')),
    path('default/', include('default.urls')),
    path('register/', include('register.urls')),
    path('sale/', include('sale.urls')),
]
