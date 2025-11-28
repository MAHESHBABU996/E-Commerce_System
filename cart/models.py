from django.db import models
from accounts.models import CustomUser
from products.models import Product

class Cart(models.Model):
    """Shopping Cart for customers."""
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_products"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.customer.username} - {self.product.name} x {self.quantity}"
 