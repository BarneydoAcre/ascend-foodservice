from django import forms

from . import models


class AddProductForm(forms.ModelForm):
    class Meta: 
        model = models.Product
        fields = [
            "company",
            "company_worker",
            "type",
            "name",
            "brand",
            "measure",
            "stock",
            "cost",
        ]

class AddProductSaleForm(forms.ModelForm):
    class Meta: 
        model = models.Product
        fields = [
            "company",
            "company_worker",
            "type",
            "name",
            "price",
        ]

class AddBrandForm(forms.ModelForm):
    class Meta:
        model = models.ProductBrand
        fields = [
            "company",
            "company_worker",
            "brand",
        ]

class AddMeasureForm(forms.ModelForm):
    class Meta:
        model = models.ProductMeasure
        fields = [
            "company",
            "company_worker",
            "measure",
        ]

class AddProductItemsForm(forms.ModelForm):
    class Meta: 
        model = models.ProductItems
        fields = [
            "company",
            "company_worker",
            "product",
            "product_item",
            "quantity",
        ]