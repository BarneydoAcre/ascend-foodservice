from django import forms

from . import models


class SaleForm(forms.ModelForm):
    class Meta: 
        model = models.Sale
        fields = [
            "company",
            "company_worker",
            "value",
            "canceled",
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
