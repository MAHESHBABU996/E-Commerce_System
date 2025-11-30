from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model

User = get_user_model()


class Supplier(models.Model):
    """Product suppliers"""
    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="suppliers",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Compliance(models.Model):
    """Vendor compliance records"""
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="compliances",
        null=True,
        blank=True
    )
    compliance_type = models.CharField(max_length=255)
    approval_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved")],
        default="Pending"
    )

    def __str__(self):
        vendor_name = self.vendor.username if self.vendor else "No Vendor"
        return f"{vendor_name} - {self.compliance_type}"


class Inventory(models.Model):
    """Product inventory (OneToOne with Product)"""
    product = models.OneToOneField(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="vendor_inventory"
    )
    quantity = models.PositiveIntegerField(default=0)
    total_stock_added = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old = Inventory.objects.get(pk=self.pk)
            added = self.quantity - old.quantity
            if added > 0:
                self.total_stock_added += added
        else:
            self.total_stock_added = self.quantity

        super().save(*args, **kwargs)

        # ✅ Sync stock to Product model
        product_model = apps.get_model("products", "Product")
        product = product_model.objects.get(id=self.product.id)
        product.stock = self.quantity
        product.save()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} in stock"


class Warehouse(models.Model):
    """Warehouses managed by vendors"""
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="warehouses"
    )

    def __str__(self):
        return self.name
