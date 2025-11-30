from django.urls import path
from . import views

app_name = 'logistics'  # Add this line to define the namespace

urlpatterns = [
    # ...existing patterns...
    path('logistics/warehouses/edit/<int:pk>/', views.edit_warehouse, name='edit_warehouse'),
    path('logistics/warehouses/', views.warehouse_list, name='warehouse_list'),
]