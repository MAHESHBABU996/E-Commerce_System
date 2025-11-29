from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Warehouse, Shipment, Fleet
from .forms import WarehouseForm, ShipmentForm, FleetForm
from accounts.decorators import role_required
from orders.models import Order  # ✅ Required to create shipment for order


# 🔹 Return Shipments View


# ✅ Return Shipments List View
@login_required
@role_required("Logistics")
def return_shipments(request):
    shipments = Shipment.objects.filter(is_return=True)
    return render(request, "logistics/return_shipments.html", {"shipments": shipments})


# ✅ Update Return Shipment Status
@login_required
@role_required("Logistics")
def update_return_shipment_status(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id, is_return=True)

    # Progress status from Pending → Shipped → Delivered
    if shipment.status != "Delivered":
        if shipment.status == "Pending":
            shipment.status = "Shipped"
        elif shipment.status == "Shipped":
            shipment.status = "Delivered"

        shipment.save()
        messages.success(request, f"Return shipment #{shipment.id} updated to {shipment.status}.")
    else:
        messages.info(request, "Return shipment is already marked as Delivered.")

    return redirect("logistics:return_shipments")















# 🔹 Logistics Dashboard
@login_required
@role_required("Logistics")
def logistics_dashboard(request):
    return render(request, "logistics/logistics_dashboard.html")


# 🔹 Warehouse Management
@login_required
@role_required("Logistics")
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'logistics/warehouse_list.html', {'warehouses': warehouses})

@login_required
@role_required("Logistics")
def edit_warehouse(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == "POST":
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse updated successfully!")
            return redirect("logistics:warehouse_list")
    else:
        form = WarehouseForm(instance=warehouse)

    return render(request, "logistics/edit_warehouse.html", {"form": form, "warehouse": warehouse})



# 🔹 Shipment Tracking
@login_required
@role_required("Logistics")
def shipment_list(request):
    shipments = Shipment.objects.all()
    return render(request, "logistics/shipment_list.html", {"shipments": shipments})

@login_required
@role_required("Logistics")
def update_shipment_status(request, shipment_id, status):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.status = status
    shipment.save()
    messages.success(request, f"Shipment #{shipment.id} updated to {shipment.status}.")
    return redirect("logistics:shipment_list") # ✅ Add namespace



# 🔹 Handle Return Shipments
@login_required
@role_required("Logistics")
def initiate_return_shipment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if not order.is_returned:
        Shipment.objects.create(
            order=order,
            warehouse=order.current_warehouse,
            status="Return Initiated",
            is_return=True
        )
        order.is_returned = True
        order.status = "Return Initiated"
        order.save()
        messages.success(request, f"Return initiated for Order #{order.id}.")
    else:
        messages.info(request, f"Return already initiated for Order #{order.id}.")

    return redirect("shipment_list")


# 🔹 Fleet Management
@login_required
@role_required("Logistics")
def fleet_list(request):
    fleet = Fleet.objects.all()
    return render(request, "logistics/fleet_list.html", {"fleet": fleet})

from django.shortcuts import render, redirect
from .forms import FleetForm

from django.shortcuts import render, redirect
from .forms import FleetForm

def add_vehicle(request):
    if request.method == 'POST':
        form = FleetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logistics:fleet_list')
    else:
        form = FleetForm()
    return render(request, 'logistics/add_vehicle.html', {'form': form})
