from django.db import models
from django.apps import apps
from django.utils import timezone

class Inventory(models.Model):
    """
    Inventory Model for Tracking Stock
    """
    product = models.OneToOneField(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="inventory"  # ✅ Use unique related_name to avoid reverse accessor clashes
    )
    quantity = models.PositiveIntegerField(default=0)  # ✅ Current available stock
    total_stock_added = models.PositiveIntegerField(default=0)  # ✅ Cumulative stock added
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save to calculate total_stock_added and sync stock to Product model
        """
        if self.pk:
            old = Inventory.objects.get(pk=self.pk)
            added = self.quantity - old.quantity
            if added > 0:
                self.total_stock_added += added
        else:
            self.total_stock_added = self.quantity

        super().save(*args, **kwargs)

        # ✅ Sync to Product model
        product_model = apps.get_model("products", "Product")
        product = product_model.objects.get(id=self.product.id)
        product.stock = self.quantity
        product.save()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"
