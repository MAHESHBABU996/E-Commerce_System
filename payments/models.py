from django.db import models
from orders.models import Order
from customers.models import Customer

class Payment(models.Model):
    """Stores payment details for an order."""
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('UPI', 'UPI'),
        ('Cash on Delivery', 'Cash on Delivery')
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

class RefundRequest(models.Model):
    """Handles customer refund requests."""
    REFUND_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="refund_requests")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund {self.id} - {self.status}"
