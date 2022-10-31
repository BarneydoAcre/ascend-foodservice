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
            "cost",
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

class AddPartnerForm(forms.ModelForm):
    class Meta: 
        model = models.Partner
        fields = [
            "company",
            "company_worker",
            "person_f_j",
            "type_client",
            "type_provider",
            "type_conveyor",
            "name",
            "fantasy",
            "cpf",
            "cnpj",
            "ie",
            "phone_number",
            "email",
            "cep",
            "street",
            "district",
            "city",
            "num",
        ]
        exclude = [
        ]