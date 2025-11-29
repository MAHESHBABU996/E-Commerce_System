from django.db import models
from accounts.models import CustomUser
from products.models import Product


class Order(models.Model):
    """Stores customer orders and tracks logistics movement."""

    STATUS_CHOICES = [
        ("Pending", "Pending"),              # Order placed by customer
        ("Accepted", "Accepted"),            # Vendor accepted
        ("Packaged", "Packaged"),            # Vendor packed
        ("Shipped", "Shipped"),              # Logistics team picked up
        ("In Transit", "In Transit"),        # Moving between warehouses
        ("Out for Delivery", "Out for Delivery"),  # Near customer
        ("Delivered", "Delivered"),          # Successfully delivered
        ("Cancelled", "Cancelled"),          # Order canceled
    ]

    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders"
    )
    vendor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="vendor_orders",
        null=True,
        blank=True,
    )
    logistics_team = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="logistics_orders",
        null=True,
        blank=True,
    )
    delivery_boy = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="delivery_orders",
        null=True,
        blank=True,
    )

    # ✅ NEW FIELDS for reverse logistics
    is_returned = models.BooleanField(default=False)
    current_warehouse = models.ForeignKey(
        "logistics.Warehouse",  # ✅ string reference avoids circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_orders"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_status(self, new_status):
        """Updates order status."""
        self.status = new_status
        self.save()

    def calculate_total_price(self):
        """Calculates the total price of the order based on items."""
        self.total_price = sum(item.price * item.quantity for item in self.order_items.all())
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.customer.username} - {self.status}"


class OrderItem(models.Model):
    """Each Order can have multiple Order Items."""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
