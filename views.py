from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Warehouse
from .forms import WarehouseForm

# ...existing code...

def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'logistics/warehouse_list.html', {'warehouses': warehouses})

def edit_warehouse(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse_list')  # Replace with the correct name of your warehouse list view
    else:
        form = WarehouseForm(instance=warehouse)
    return render(request, 'logistics/edit_warehouse.html', {'form': form})

