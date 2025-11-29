from django.urls import path
from . import views

app_name = "logistics"

urlpatterns = [
    # Dashboard
    path("dashboard/", views.logistics_dashboard, name="dashboard"),

    # Warehouse Management
    path("warehouses/", views.warehouse_list, name="warehouse_list"),
    path("warehouses/edit/<int:warehouse_id>/", views.edit_warehouse, name="edit_warehouse"),


    # Shipment Tracking
    path("shipments/", views.shipment_list, name="shipment_list"),
    
    path("shipments/update/<int:shipment_id>/<str:status>/", views.update_shipment_status, name="update_shipment_status"),

    # Return Shipments
    path("shipments/return/", views.return_shipments, name="return_shipments"),
    path("shipments/return/<int:shipment_id>/update/", views.update_return_shipment_status, name="update_return_shipment_status"),

    

    



    # Fleet Management
    path('fleet/', views.fleet_list, name='fleet_list'),
    path('fleet/add/', views.add_vehicle, name='add_vehicle'), 
    
]
