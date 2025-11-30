from django.db import models
from accounts.models import CustomUser  # ✅ Vendor reference


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Model for Vendors"""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="vendor_products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    total_stock_added = models.PositiveIntegerField(default=0)
    current_stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    APPROVAL_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # 🔹 Stock Management Methods
    def add_stock(self, quantity):
        """Add new stock to the product"""
        self.total_stock_added += quantity
        self.current_stock += quantity
        self.save(update_fields=["total_stock_added", "current_stock", "updated_at"])

    def reduce_stock(self, quantity):
        """Reduce stock when product is purchased"""
        if self.current_stock >= quantity:
            self.current_stock -= quantity
            self.save(update_fields=["current_stock", "updated_at"])
        else:
            raise ValueError("Not enough stock available.")

    def return_stock(self, quantity):
        """Restock the product on return"""
        self.current_stock += quantity
        self.save(update_fields=["current_stock", "updated_at"])
