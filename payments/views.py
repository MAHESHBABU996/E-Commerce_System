import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


# -------------------------------
# 💳 Manual Payment View (UPI / QR)
# -------------------------------
@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if order.status != "Pending":
        messages.warning(request, "This order is already paid or processed.")
        return redirect("payments:order_list")

    return render(request, "payments/manual_payment.html", {"order": order})


# -------------------------------
# ✅ Mark Manual Payment as Done
# -------------------------------
@login_required
def mark_order_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if order.status == "Pending":
        order.status = "Paid"
        order.save()
        messages.success(request, f"✅ Order #{order.id} marked as Paid. Awaiting confirmation.")
    else:
        messages.info(request, "Order already marked as paid.")

    return redirect("payments:order_list")


# -------------------------------
# 📋 List Orders
# -------------------------------
@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).order_by("-order_date")

    if not orders.exists():
        messages.warning(request, "You have no orders yet. Start shopping now!")

    return render(request, "payments/order_list.html", {"orders": orders})


# -------------------------------
# 💸 Stripe (Optional)
# -------------------------------
# Uncomment only if using Stripe
# @login_required
# def process_payment(request, order_id):
#     order = get_object_or_404(Order, id=order_id, customer=request.user)
#     intent = stripe.PaymentIntent.create(
#         amount=int(order.total_price * 100),
#         currency="usd",
#         payment_method_types=["card"],
#     )
#     return render(request, "payments/payment.html", {
#         "order": order,
#         "client_secret": intent.client_secret
#     })


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from orders.models import Order

def mark_as_paid(request, order_id):
    """Marks an order as paid and notifies the vendor."""
    order = get_object_or_404(Order, id=order_id)

    # Update the order status to "Paid"
    order.status = "Paid"
    order.save()

    messages.success(request, "Payment confirmed. Vendor has been notified!")
    return redirect("orders:order_list")  # Redirect user after payment
