from django.db import models
from django.apps import apps  # ✅ Avoid circular import
from accounts.models import CustomUser

# 🔹 Warehouse Model
class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.location})"


# 🔹 Shipment Model
class Shipment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Return Initiated", "Return Initiated"),
        ("Returning", "Returning"),
        ("Returned to Vendor", "Returned to Vendor"),
    ]
    
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="shipment"
    )  # ✅ Use string reference to avoid circular import

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    tracking_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_return = models.BooleanField(default=False)  # ✅ Added to support return shipments

    def __str__(self):
        return f"Shipment {self.id} - {self.status}{' (Return)' if self.is_return else ''}"

    def get_order(self):
        """Fetch the Order object dynamically to avoid circular import issues."""
        Order = apps.get_model("orders", "Order")  # ✅ Correct way to avoid import issues
        return Order.objects.get(id=self.order_id)


# 🔹 Fleet Model 
class Fleet(models.Model):
    vehicle_name = models.CharField(max_length=255)
    license_plate = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()

    assigned_driver = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role__name": "Logistics"}  # ✅ Only allow logistics users
    )

    def __str__(self):
        return f"{self.vehicle_name} ({self.license_plate})"
