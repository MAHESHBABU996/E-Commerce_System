# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.apps import apps

# def add_to_cart(request, product_id):
#     """Add a product to the cart."""
#     product = get_object_or_404(Product, id=product_id)

#     cart_item, created = Cart.objects.get_or_create(
#         customer=request.user,
#         product=product
#     )
#     if not created:
#         cart_item.quantity += 1 
#         cart_item.save()
    
#     messages.success(request, f"{product.name} added to cart!")
#     return redirect(reverse("cart:view_cart"))
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))  # Allow users to set quantity

    cart_item, created = Cart.objects.get_or_create(
        customer=request.user, product=product
    )
    if not created:
        cart_item.quantity += quantity  # ✅ Update dynamically
        cart_item.save()
    
    messages.success(request, f"{product.name} added to cart!")
    return redirect(reverse("cart:view_cart"))


@login_required
def view_cart(request):
    """Display the user's shopping cart."""
    cart_items = request.user.cart_items.all()  # Fetch cart items
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # ✅ Ensure correct calculation

    # Determine Dashboard URL based on user role
    if request.user.is_vendor():
        dashboard_url = "vendor_dashboard"
    elif request.user.is_customer():
        dashboard_url = "customer_dashboard"
    else:
        dashboard_url = "home"

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,  # ✅ Pass total price to template
        "dashboard_url": dashboard_url,
        "clear_cart_url": reverse("cart:clear_cart"),  # ✅ Use namespace for clear_cart
    })

@login_required
def remove_from_cart(request, item_id):  # ✅ Changed parameter name to match URL pattern
    cart_item = get_object_or_404(Cart, id=item_id)
    cart_item.delete()
    return redirect("cart:view_cart")  # ✅ Ensure correct namespace
from django.db import transaction

@login_required
def checkout(request):
    """Handles the checkout process and creates an order."""
    from django.db import transaction
    from django.apps import apps

    Cart = apps.get_model("cart", "Cart")
    Order = apps.get_model("orders", "Order")
    OrderItem = apps.get_model("orders", "OrderItem")

    cart_items = Cart.objects.filter(customer=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("cart:view_cart")  # ✅ Redirect if cart is empty
 
    # ✅ Print cart item details for debugging
    print(f"🛒 Cart Items for {request.user.username}:")
    for item in cart_items:
        print(f"   - {item.quantity} x {item.product.name} = ${item.product.price * item.quantity}")

    total_price = sum(item.product.price * item.quantity for item in cart_items)  # ✅ Ensure correct total price calculation
    print(f"💰 Calculated Total Price: ${total_price}")  # ✅ Debugging total

    if request.method == "POST":
        with transaction.atomic():
            order = Order.objects.create(
                customer=request.user,
                total_price=total_price,  # ✅ Save correct total price
                status="Pending"
            )
            print(f"✅ Order Created: {order.id} - Total: ${order.total_price}")

            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            cart_items.delete()  # ✅ Clear cart after order placement

            messages.success(request, "Order placed successfully!")
            return redirect("orders:order_list")  

    return render(request, "orders/checkout.html", {"cart_items": cart_items})



@login_required
def clear_cart(request):
    """Removes all items from the user's cart."""
    Cart.objects.filter(customer=request.user).delete()
    return redirect("cart:view_cart")  # ✅ Use namespace for view_cart

@login_required
def update_cart(request, item_id):
    """Update the quantity of a cart item."""
    cart_item = get_object_or_404(Cart, id=item_id, customer=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated quantity for {cart_item.product.name}.")
        else:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from cart.")
    return redirect("cart:view_cart")



