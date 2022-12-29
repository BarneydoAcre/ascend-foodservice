from django.db import models
from django.contrib.auth.models import User

import default.models
import register.models

     
class Sale(models.Model):
    company = models.ForeignKey(default.models.Company, on_delete=models.PROTECT)
    company_worker = models.ForeignKey(default.models.CompanyWorker, on_delete=models.PROTECT)
    value = models.FloatField(blank=False)
    delivery = models.FloatField(blank=False, default=0)
    canceled = models.BooleanField(default=False)
    total = models.FloatField(blank=True, null=True, default=0)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name, verbose_name_plural = "Venda", "Vendas"
        ordering = ("company","id",)

class SaleItems(models.Model):
    company = models.ForeignKey(default.models.Company, on_delete=models.PROTECT)
    company_worker = models.ForeignKey(default.models.CompanyWorker, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    product = models.ForeignKey(register.models.Product, on_delete=models.PROTECT)
    quantity = models.FloatField(blank=False, default=0)
    price = models.FloatField(blank=False, default=0)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name, verbose_name_plural = "Venda Items", "Vendas Items"
        ordering = ("company","product",)
