from django.urls import path
from .views import order_list, pay_order, mark_order_paid
# Optional: Import Stripe view if you're using it
# from .views import process_payment

app_name = "payments"  # Namespace for use in {% url 'payments:xyz' %}

urlpatterns = [
    path("orders/", order_list, name="order_list"),                    # 🧾 View all orders
    path("pay/<int:order_id>/", pay_order, name="pay_order"),         # 💳 Show manual payment (UPI, etc.)
    path("paid/<int:order_id>/", mark_order_paid, name="mark_order_paid"),  # ✅ Customer confirms payment

    # Optional Stripe integration (uncomment when needed)
    # path("stripe/<int:order_id>/", process_payment, name="process_payment"),
]


