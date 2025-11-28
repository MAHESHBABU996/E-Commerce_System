from django import forms
from inventory.models import Inventory

class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['total_stock_added', 'quantity']
