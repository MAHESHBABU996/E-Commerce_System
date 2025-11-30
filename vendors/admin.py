from django.contrib import admin
from .models import Supplier, Compliance, Inventory, Warehouse

admin.site.register(Supplier)
admin.site.register(Compliance)
admin.site.register(Inventory)
admin.site.register(Warehouse)
