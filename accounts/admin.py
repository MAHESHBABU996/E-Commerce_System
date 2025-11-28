from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, VendorType
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser model."""

    # Specify the forms to add and change user instances
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Define the fields to display in the admin panel
    list_display = ("username", "email", "phone", "role", "vendor_type", "is_role_approved", "is_staff", "is_active")
    list_filter = ("role", "vendor_type", "is_role_approved", "is_staff", "is_active")

    # Define the fieldsets for viewing and editing users
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone", "address")}),
        ("Role & Approval", {"fields": ("role", "vendor_type", "is_role_approved")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("date_joined", "last_login")}),
    )

    # Define the fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "address", "role", "vendor_type", "is_role_approved", 
                       "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "email", "phone")
    ordering = ("username",)

class RoleAdmin(admin.ModelAdmin):
    """Admin panel configuration for Role model."""
    list_display = ("name",)
    search_fields = ("name",)

class VendorTypeAdmin(admin.ModelAdmin):
    """Admin panel configuration for VendorType model."""
    list_display = ("name",)
    search_fields = ("name",)

# Register the models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(VendorType, VendorTypeAdmin)
