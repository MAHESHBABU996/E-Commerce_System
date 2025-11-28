from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    ADMIN = "Admin"
    VENDOR = "Vendor"
    CUSTOMER = "Customer"
    LOGISTICS = "Logistics"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (VENDOR, "Vendor"),
        (CUSTOMER, "Customer"),
        (LOGISTICS, "Logistics"),
    ]

    name = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

class VendorType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name  # Fixed syntax error

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    vendor_type = models.ForeignKey(VendorType, null=True, blank=True, on_delete=models.SET_NULL)

    is_role_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Automatically approve Customers, but require approval for Vendors & Logistics.
        """
        if not self.pk:  # Only apply on new user creation 
            if self.role and self.role.name == Role.CUSTOMER:
                self.is_role_approved = True
            else:
                self.is_role_approved = False
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.role and self.role.name == Role.ADMIN

    def is_vendor(self):
        return self.role and self.role.name == Role.VENDOR

    def is_customer(self):
        return self.role and self.role.name == Role.CUSTOMER

    def is_logistics(self):
        return self.role and self.role.name == Role.LOGISTICS

    def __str__(self):
        return f"{self.username} ({self.role.name if self.role else 'No Role'})"
