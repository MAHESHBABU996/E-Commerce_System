from django.contrib import admin
from .models import Warehouse, Shipment, Fleet

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "capacity"]
    search_fields = ["name", "location"]

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "warehouse", "status", "tracking_number", "is_return"]
    list_filter = ["status", "is_return"]
    search_fields = ["tracking_number"]

@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ["vehicle_name", "license_plate", "capacity", "assigned_driver"]
    search_fields = ["vehicle_name", "license_plate"]
