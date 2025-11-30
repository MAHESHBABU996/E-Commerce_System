# reviews/urls.py

from django.urls import path
from .views import index  # Import views directly without any indirect imports

urlpatterns = [
    path('', index, name='review_index'),
]
