from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.apps import apps
from django.contrib.auth import get_user_model

from accounts.decorators import role_required
from orders.models import Order, OrderItem
from logistics.models import Shipment
from inventory.models import Inventory
from .forms import ProductForm, InventoryUpdateForm
from .models import Supplier

Product = apps.get_model("products", "Product")
User = get_user_model()

# 🔹 Vendor Dashboard
@login_required
@role_required("Vendor")
def vendor_dashboard(request):
    products = Product.objects.filter(vendor=request.user)
    product_ids = products.values_list("id", flat=True)
    order_items = OrderItem.objects.filter(product_id__in=product_ids)
    orders = Order.objects.filter(id__in=order_items.values_list("order_id", flat=True)).distinct()
    return render(request, "vendors/vendor_dashboard.html", {"products": products, "orders": orders})


# 🔹 Product Management
@login_required
@role_required("Vendor")
def vendor_product_list(request):
    products = Product.objects.filter(vendor=request.user).order_by("approval_status").prefetch_related("inventory")
    for product in products:
        product.stock = product.inventory.quantity if hasattr(product, "inventory") else 0
    return render(request, "vendors/vendor_product_list.html", {"products": products})


@login_required
@role_required("Vendor")
def vendor_add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            Inventory.objects.create(product=product, quantity=0)
            messages.success(request, "Product added successfully!")
            return redirect("vendors:vendor_product_list")
    else:
        form = ProductForm()
    return render(request, "vendors/vendor_add_product.html", {"form": form})


@login_required
@role_required("Vendor")
def vendor_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, vendor=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("vendors:vendor_product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "vendors/vendor_edit_product.html", {"form": form})


@login_required
@role_required("Vendor")
def vendor_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, vendor=request.user)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("vendors:vendor_product_list")




@login_required
@role_required("Vendor")
def vendor_update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    products = Product.objects.filter(vendor=request.user)

    if not OrderItem.objects.filter(order=order, product__in=products).exists():
        messages.error(request, "You do not have permission to update this order.")
        return redirect("vendors:vendor_order_list")

    order.status = status
    order.save()

    if status == "Shipped":
        shipment, created = Shipment.objects.get_or_create(order=order)
        if created:
            messages.success(request, f"Order {order.id} is now shipped! Shipment created.")
        else:
            messages.warning(request, f"Shipment for Order {order.id} already exists.")

    return redirect("vendors:vendor_order_list")


# 🔹 Inventory View
# @login_required
# @role_required("Vendor")
# def inventory_view(request):
#     inventories = Inventory.objects.select_related('product').filter(product__vendor=request.user)
#     return render(request, 'vendors/inventory.html', {'products': inventories})

# vendors/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product

# @login_required
# def inventory_view(request):
#     vendor = request.user
#     inventory_items = Product.objects.filter(vendor=vendor)

#     return render(request, 'vendors/inventory.html', {
#         'inventory_items': inventory_items
#     })

from products.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def inventory_view(request):
    vendor = request.user
    inventory_items = Product.objects.filter(vendor=vendor, is_active=True, approval_status="Approved")
    return render(request, 'vendors/inventory.html', {'inventory_items': inventory_items})



# 🔹 Inventory Update
# @login_required
# @role_required("Vendor")
# def update_inventory(request, product_id):
#     product = get_object_or_404(Product, id=product_id, vendor=request.user)
#     inventory = get_object_or_404(Inventory, product=product)

#     if request.method == 'POST':
#         form = InventoryUpdateForm(request.POST)
#         if form.is_valid():
#             new_quantity = form.cleaned_data['stock']

#             if new_quantity > inventory.quantity:
#                 added = new_quantity - inventory.quantity
#                 inventory.quantity = new_quantity
#                 inventory.total_stock_added += added
#             elif new_quantity < inventory.quantity:
#                 inventory.quantity = new_quantity

#             inventory.save()
#             messages.success(request, "Inventory updated successfully.")
#             return redirect("vendors:inventory")
#     else:
#         form = InventoryUpdateForm(initial={'stock': inventory.quantity})

#     return render(request, "vendors/update_inventory.html", {"form": form, "product": product})

# vendors/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .forms import ProductInventoryForm

@login_required
def update_inventory(request, product_id):
    product = get_object_or_404(Product, id=product_id, vendor=request.user)

    if request.method == 'POST':
        form = ProductInventoryForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendors:inventory')
    else:
        form = ProductInventoryForm(instance=product)

    return render(request, 'vendors/update_inventory.html', {
        'form': form,
        'product': product
    })



# 🔹 Supplier Management
@login_required
@role_required("Vendor")
def vendor_supplier_list(request):
    vendor = request.user
    suppliers = Supplier.objects.filter(vendor=vendor)
    return render(request, "vendors/vendor_supplier_list.html", {"suppliers": suppliers})


# 🔹 Product Approval (Admin Only)
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def approve_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.approval_status = "Approved"
    product.save()
    messages.success(request, f"{product.name} approved successfully.")
    return redirect("vendors:pending_products")


@staff_member_required
def reject_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.approval_status = "Rejected"
    product.save()
    messages.error(request, f"{product.name} rejected.")
    return redirect("vendors:pending_products")


@staff_member_required
def pending_products(request):
    pending_products = Product.objects.filter(approval_status='Pending')
    approved_products = Product.objects.filter(approval_status='Approved')
    return render(request, 'vendors/admin/pending_products.html', {
        'pending_products': pending_products,
        'approved_products': approved_products,
    })


# # 🔹 All Orders View for Vendor
# vendors/views.py
# vendors/views.py

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.http import HttpResponseForbidden
# from orders.models import OrderItem

# @login_required
# def all_orders_view(request):
#     user = request.user

#     # Allow only vendors and admins (case-insensitive check)
#     if user.role not in ["Vendor", "Admin"]:
#         return HttpResponseForbidden("You are not authorized to view this page.")

#     # Vendor: see only their product orders
#     if user.role == "Vendor":
#         order_items = OrderItem.objects.filter(product__vendor=user) \
#             .select_related('order', 'product') \
#             .order_by('-order__created_at')
#     else:
#         # Admin: see all orders
#         order_items = OrderItem.objects.all() \
#             .select_related('order', 'product', 'product__vendor') \
#             .order_by('-order__created_at')

#     return render(request, 'vendors/all_orders.html', {
#         'order_items': order_items,
#         'is_admin': user.role.lower() == "admin"
#     })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from products.models import Product
from orders.models import OrderItem, Order
# from utils.decorators import role_required  # Make sure you have this or replace with logic inline

@login_required
@role_required("Vendor")
def vendor_order_list(request):
    user = request.user
    products = Product.objects.filter(vendor=user)
    product_ids = products.values_list("id", flat=True)
    order_items = OrderItem.objects.filter(product_id__in=product_ids)

    # We group by orders that include vendor's products
    orders = Order.objects.filter(id__in=order_items.values_list("order_id", flat=True)).distinct().order_by('-order_date')


    return render(request, "vendors/vendor_order_list.html", {
        "orders": orders,
        "order_items": order_items,
    })



# vendors/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from orders.models import OrderItem

@login_required
def all_orders_view(request):
    user = request.user

    if user.role not in ["vendor", "admin"]:
        return redirect("vendors:vendor_dashboard")  # Or use a 403 page

    if user.role == "vendor":
        order_items = OrderItem.objects.filter(product__vendor=user)
    else:  # Admin
        order_items = OrderItem.objects.all()

    return render(request, "vendors/all_orders.html", {"order_items": order_items})
