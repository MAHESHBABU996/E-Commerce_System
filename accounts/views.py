from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import CustomUser, Role, VendorType
from .decorators import role_required
from .forms import (
    CustomUserEditForm,
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomSignupForm,
)

from orders.models import Order  # For customer_dashboard

# 🔹 Home Page View
def home(request):
    return render(request, "home.html")

# 🔹 Signup View
def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Ensure Vendor selects a Vendor Type
            if user.role.name == "Vendor" and not user.vendor_type:
                messages.error(request, "Vendors must select a Vendor Type.")
                return render(request, "accounts/signup.html", {"form": form})

            # Auto-approve Customers
            if user.role.name == "Customer":
                user.is_role_approved = True

            user.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect_dashboard(user)
    else:
        form = CustomSignupForm()
    return render(request, "accounts/signup.html", {"form": form})

# 🔹 Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            if not user.role:
                messages.error(request, "Your account does not have a role assigned. Please contact support.")
                return redirect("login")

            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect_dashboard(user)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")

# 🔹 Logout View
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

# 🔹 Redirect users based on their role
def redirect_dashboard(user):
    role_redirects = {
        "Admin": "admin_dashboard",
        "Vendor": "vendor_dashboard",
        "Customer": "customer_dashboard",
        "Logistics": "logistics_dashboard",
    }
    return redirect(role_redirects.get(user.role.name, "customer_dashboard"))

# 🔹 Admin Dashboard
@login_required
@role_required("Admin")
def admin_dashboard(request):
    users = CustomUser.objects.all()
    vendor_types = VendorType.objects.all()
    return render(request, "accounts/admin_dashboard.html", {"users": users, "vendor_types": vendor_types})

# 🔹 Vendor Dashboard
@login_required
@role_required("Vendor")
def vendor_dashboard(request):
    return render(request, "vendors/vendor_dashboard.html")

# 🔹 Customer Dashboard - shows user's orders with products
@login_required
@role_required("Customer")
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related("order_items__product")
    view_cart_url = reverse("cart:view_cart")
    return render(request, "accounts/customer_dashboard.html", {
        "orders": orders,
        "view_cart_url": view_cart_url,
    })

# 🔹 Logistics Dashboard
@login_required
@role_required("Logistics")
def logistics_dashboard(request):
    return render(request, "logistics/logistics_dashboard.html")


# 🔹 Order List View (Customers only)
@login_required
@role_required("Customer")
def order_list(request):
    return render(request, "accounts/order_list.html")

# 🔹 Approve User (Admin Only)
@login_required
@role_required("Admin")
def approve_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_role_approved:
        messages.info(request, f"{user.username} is already approved.")
    else:
        user.is_role_approved = True
        user.save(update_fields=["is_role_approved"])
        messages.success(request, f"{user.username} has been approved successfully!")
    return redirect("admin_dashboard")

# 🔹 Remove User (Admin Only)
@login_required
@role_required("Admin")
def remove_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, f"User {user.username} has been removed.")
    return redirect("admin_dashboard")

# 🔹 Edit User (Admin Only)
@login_required
@role_required("Admin")
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username}'s information has been updated.")
            return redirect("admin_dashboard")
    else:
        form = CustomUserEditForm(instance=user)
    return render(request, "accounts/edit_user.html", {"form": form, "user": user})

# 🔹 Add User (Admin Only)
@login_required
@role_required("Admin")
def add_user_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully!")
            return redirect("admin_dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/add_user.html", {"form": form})

# 🔹 Vendor Type Management (Admin Only)
@login_required
@role_required("Admin")
def add_vendor_type(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            VendorType.objects.create(name=name)
            messages.success(request, f"Vendor Type '{name}' added successfully!")
    return redirect("admin_dashboard")

@login_required
@role_required("Admin")
def delete_vendor_type(request, vendor_type_id):
    vendor_type = get_object_or_404(VendorType, id=vendor_type_id)
    vendor_type.delete()
    messages.success(request, f"Vendor Type '{vendor_type.name}' deleted successfully!")
    return redirect("admin_dashboard")

# 🔹 Error Pages
def page_403(request):
    return render(request, "accounts/403.html")

def page_404(request, exception=None):
    return render(request, "accounts/404.html", status=404)
