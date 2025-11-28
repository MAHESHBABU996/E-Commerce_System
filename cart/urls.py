from django.urls import path
from .views import view_cart, add_to_cart, remove_from_cart, clear_cart, checkout, update_cart

app_name = 'cart'  # Register the namespace

urlpatterns = [
    path("", view_cart, name="view_cart"),  # ✅ View cart
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),  # ✅ Add product
    path("remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),  # ✅ Remove product
    path("clear/", clear_cart, name="clear_cart"),  # ✅ Clear all cart items
    path("checkout/", checkout, name="checkout"),  # ✅ Proceed to checkout  
    path("update/<int:item_id>/", update_cart, name="update_cart"),  # ✅ Update cart item
]
