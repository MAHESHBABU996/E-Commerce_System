from django import forms
from products.models import Product
from inventory.models import Inventory
from .models import Supplier


# 🔹 Product Form (For Vendors to Add/Edit Products)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "image"]


# 🔹 Inventory Form (If inventory is created manually)
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["product", "quantity"]


# 🔹 Inventory Update Form (Used for updating quantity only)
class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["quantity"]  # Only editable quantity, stock tracking is via Product model


# 🔹 Product Inventory Form (For updating current stock in Product model)
class ProductInventoryForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["current_stock"]


# 🔹 Supplier Form (Vendor's Suppliers)
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_info"]
