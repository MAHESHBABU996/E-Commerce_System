# products/admin.py

from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
 list_display = ('name', 'vendor',  'price', 'current_stock', 'is_active', 'approval_status', 'updated_at')
 list_filter = ('category', 'is_active', 'approval_status')
 search_fields = ('name', 'vendor__username')
 ordering = ('-updated_at',)
