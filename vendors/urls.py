from django.urls import path
from .views import (
    vendor_dashboard,
    all_orders_view,
    approve_product,
    pending_products,
    reject_product,
    vendor_product_list,
    vendor_add_product,
    vendor_edit_product,
    vendor_delete_product,
    vendor_order_list,
    vendor_update_order_status,
    vendor_supplier_list,
    inventory_view,
    update_inventory,
)

app_name = "vendors"  # Enables {% url 'vendors:...' %} in templates

urlpatterns = [
    # 🔹 Vendor Dashboard
    path("vendor-dashboard/", vendor_dashboard, name="vendor_dashboard"),

    # 🔹 Orders
    # path("orders/all/", all_orders_view, name="all_orders"),
    path("orders/list/", vendor_order_list, name="vendor_order_list"),
    path("orders/update-status/<int:order_id>/<str:status>/", vendor_update_order_status, name="vendor_update_order_status"),
    # path("orders/list/", all_orders_view, name="all_orders"),
    path('orders/', all_orders_view, name='all_orders'),
    # path("orders/update/<int:order_id>/<str:status>/", vendor_update_order_status, name="vendor_update_order_status"),

    # 🔹 Product Management
    path("products/", vendor_product_list, name="vendor_product_list"),
    path("products/add/", vendor_add_product, name="vendor_add_product"),
    path("products/edit/<int:product_id>/", vendor_edit_product, name="vendor_edit_product"),
    path("products/delete/<int:product_id>/", vendor_delete_product, name="vendor_delete_product"),

    # 🔹 Product Approval (Admin)
    path("admin/pending-products/", pending_products, name="pending_products"),
    path("admin/approve-product/<int:product_id>/", approve_product, name="approve_product"),
    path("admin/reject-product/<int:product_id>/", reject_product, name="reject_product"),

    # 🔹 Inventory Management
    path("inventory/", inventory_view, name="inventory"),
    path("inventory/update/<int:product_id>/", update_inventory, name="update_inventory"),

    # 🔹 Supplier Management
    path("suppliers/", vendor_supplier_list, name="vendor_supplier_list"),
    
]
