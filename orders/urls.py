from django.urls import path
from . import views  # ✅ Correct relative import

app_name = "orders"

urlpatterns = [
    # ✅ Customer actions
    path("checkout/", views.checkout, name="checkout"),
    path("place/", views.place_order, name="place_order"),
    path("", views.order_list, name="order_list"),
    path("<int:order_id>/", views.order_details, name="order_details"),
    path("<int:order_id>/update/", views.update_order, name="update_order"),
    path("<int:order_id>/invoice/", views.download_invoice, name="download_invoice"),
    path("orders/<int:order_id>/return/", views.return_order, name="return_order"),
    path('orders/<int:order_id>/return/', views.return_order, name='return_order'),

    # ✅ Vendor actions
    path("vendor/accept/<int:order_id>/", views.vendor_accept_order, name="vendor_accept_order"),
    path("vendor/pack/<int:order_id>/", views.vendor_pack_order, name="vendor_pack_order"),

    # ✅ Logistics actions
    path("logistics/ship/<int:order_id>/", views.logistics_ship_order, name="logistics_ship_order"),

    # ✅ Delivery actions
    path("delivery/deliver/<int:order_id>/", views.delivery_boy_deliver_order, name="delivery_boy_deliver_order"),
    # path('orders/all/', views.all_orders_view, name='all_orders'),

    
]
