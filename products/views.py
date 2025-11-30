from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Product
from inventory.models import Inventory

User = get_user_model()


# 🔹 Product List View
@login_required
def product_list(request):
    """Display the list of available products for customers & vendors."""
    products = Product.objects.filter(is_active=True, approval_status="Approved")  # Only show approved & active

    # Determine dashboard redirect based on user role
    dashboard_url = "customer_dashboard"
    if hasattr(request.user, "is_vendor") and request.user.is_vendor():
        dashboard_url = "vendor_dashboard"

    return render(request, "products/product_list.html", {
        "products": products,
        "dashboard_url": dashboard_url,
    })


# 🔹 Product Detail View
@login_required
def product_detail(request, product_id):
    """Display details of a single product (Only Approved & Active)."""
    product = get_object_or_404(Product, id=product_id, is_active=True, approval_status="Approved")
    return render(request, "products/product_detail.html", {"product": product})


# 🔹 Inventory View (Optional: This is better suited to `vendors/views.py`)
@login_required
def inventory_view(request):
    """Vendor's inventory view (moved here by mistake — better in vendors app)."""
    if not hasattr(request.user, "is_vendor") or not request.user.is_vendor():
        return render(request, "403.html")  # Optional: restrict non-vendors

    inventory_items = Inventory.objects.filter(product__vendor=request.user)
    return render(request, 'vendors/inventory.html', {'products': inventory_items})
