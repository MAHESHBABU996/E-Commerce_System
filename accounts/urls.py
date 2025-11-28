from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 🔹 Authentication
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # 🔹 Dashboards
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("vendor-dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    
    path("customer-dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("logistics-dashboard/", views.logistics_dashboard, name="logistics_dashboard"),

    # 🔹 User Management (Admin Only)
    path("admin/approve/<int:user_id>/", views.approve_user, name="approve_user"),
    path("admin/remove/<int:user_id>/", views.remove_user, name="remove_user"),
    path("admin/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("add-user/", views.add_user_view, name="add_user"),

    # 🔹 Vendor Type Management (Admin Only)
    path("admin/add-vendor-type/", views.add_vendor_type, name="add_vendor_type"),
    path("admin/delete-vendor-type/<int:vendor_type_id>/", views.delete_vendor_type, name="delete_vendor_type"),

    # 🔹 Orders (Customer Only)
    path("orders/", views.order_list, name="order_list"),

    # 🔹 Password Reset
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),

    # 🔹 Error Pages
    path("403/", views.page_403, name="403"),
    path("404/", views.page_404, name="404"),

    # 🔹 Home
    path("", views.home, name="home"),
]
