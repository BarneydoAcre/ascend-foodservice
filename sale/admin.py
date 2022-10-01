from django.contrib import admin
from . import models


class SaleAdmin(admin.ModelAdmin):
    list_display = ("company", "id", "value", "delivery",)
admin.site.register(models.Sale, SaleAdmin)

class SaleItemsAdmin(admin.ModelAdmin):
    list_display = ("company", "product", "price", "quantity")
admin.site.register(models.SaleItems, SaleItemsAdmin)
