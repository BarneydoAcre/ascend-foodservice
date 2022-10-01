from django.db import models
from django.contrib.auth.models import User

import default.models


class ProductMeasure(models.Model):
    company = models.ForeignKey(default.models.Company, on_delete=models.PROTECT)
    company_worker = models.ForeignKey(default.models.CompanyWorker, on_delete=models.PROTECT)
    measure = models.CharField(max_length=2, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.measure

    class Meta:
        verbose_name, verbose_name_plural = "Unidade de Medida", "Unidades de Medida"

class ProductBrand(models.Model):
    company = models.ForeignKey(default.models.Company, on_delete=models.PROTECT)
    company_worker = models.ForeignKey(default.models.CompanyWorker, on_delete=models.PROTECT)
    brand = models.CharField(max_length=20, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand 

    class Meta:
        verbose_name, verbose_name_plural = "Marca do Produto", "Marca dos Produtos"
        ordering = ("brand",)

class Product(models.Model):
    c = (
        (1, "Consumo",),
        (2, "Revenda",),
    )
    company = models.ForeignKey(default.models.Company, on_delete=models.PROTECT)
    company_worker = models.ForeignKey(default.models.CompanyWorker, on_delete=models.PROTECT)
    type = models.IntegerField(choices=c, blank=False)
    name = models.CharField(max_length=50, blank=False)
    brand = models.ForeignKey(ProductBrand, on_delete=models.PROTECT, blank=True, null=True)
    measure = models.ForeignKey(ProductMeasure, on_delete=models.PROTECT, blank=True, null=True)
    stock = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = "Produto", "Produtos"
        ordering = ("name",)

class ProductItems(models.Model):
    company = models.ForeignKey(default.models.Company, on_delete=models.PROTECT)
    company_worker = models.ForeignKey(default.models.CompanyWorker, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_item = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_items")
    quantity = models.FloatField(blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_item.name

    class Meta:
        verbose_name, verbose_name_plural = "Produto Item", "Produto Items"
        ordering = ("product",)

class Groups(models.Model):
    name = models.CharField(max_length=15, default='')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name, verbose_name_plural = "Grupo", "Grupos"
        ordering = ("name",)
