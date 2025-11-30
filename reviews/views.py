# reviews/views.py

from django.shortcuts import render

# Ensure that the view function exists
def index(request):
    return render(request, 'reviews/index.html')  # Make sure this template exists
