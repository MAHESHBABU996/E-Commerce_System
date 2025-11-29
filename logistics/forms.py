from django import forms
from .models import Warehouse, Shipment, Fleet

# 🔹 Warehouse Form
class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "location", "capacity"]

# 🔹 Shipment Form 
class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["order", "warehouse", "status", "tracking_number"]

# 🔹 Fleet Form
from django import forms
from .models import Fleet

class FleetForm(forms.ModelForm):
    class Meta:
        model = Fleet
        fields = ['vehicle_name', 'license_plate', 'capacity', 'assigned_driver']

