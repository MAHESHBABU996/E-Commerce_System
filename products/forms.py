from django import forms
from .models import Product, Category, Supplier

class ProductForm(forms.ModelForm):
    """Form for adding/editing products"""
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", required=True)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), empty_label="Select Supplier", required=True)

    class Meta:
        model = Product
        fields = ["name", "category", "supplier", "price", "stock", "image","is_active"]
