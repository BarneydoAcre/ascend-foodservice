from django import forms

from . import models


class AddSaleForm(forms.ModelForm):
    class Meta: 
        model = models.Sale
        fields = [
            "company",
            "company_worker",
            "value",
            "delivery",
            "total",
        ]

class AddSaleItemsForm(forms.ModelForm):
    class Meta: 
        model = models.SaleItems
        fields = [
            "company",
            "company_worker",
            "sale",
            "product",
            "quantity",
            "price",
        ]
