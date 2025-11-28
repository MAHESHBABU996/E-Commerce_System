from django.shortcuts import redirect

class RoleBasedAccessMiddleware:
    """
    Middleware to restrict access to dashboards based on user roles.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.role_based_routes = {
            "Admin": "/accounts/admin-dashboard/",
            "Vendor": "/accounts/vendor-dashboard/",
            "Customer": "/accounts/customer-dashboard/",
            "Logistics": "/accounts/logistics-dashboard/",
        }

    def __call__(self, request):
        if request.user.is_authenticated and request.user.role:
            for role, path in self.role_based_routes.items():
                if request.path.startswith(path) and request.user.role.name != role:
                    return redirect("403")

        return self.get_response(request)

