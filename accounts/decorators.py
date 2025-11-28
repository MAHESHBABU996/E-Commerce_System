from django.shortcuts import redirect
from functools import wraps

def role_required(*role_names):
    """
    Decorator to restrict access to views based on user roles.
    Allows multiple roles (e.g., @role_required("Admin", "Vendor")). 
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role and request.user.role.name in role_names:
                return view_func(request, *args, **kwargs)
            return redirect("403")  # Redirect to '403' if unauthorized
        return _wrapped_view
    return decorator
