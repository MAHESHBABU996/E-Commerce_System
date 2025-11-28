# inventory/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventory
from products.models import Product

@receiver(post_save, sender=Inventory)
def update_product_stock(sender, instance, **kwargs):
    product = instance.product
    product.current_stock = instance.quantity
    product.save()
