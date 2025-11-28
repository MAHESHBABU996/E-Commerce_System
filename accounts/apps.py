from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_migrate

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from .models import Role  # Import inside to prevent circular imports

        def create_roles(sender, **kwargs):
            """
            Ensure predefined roles exist after migrations.
            """
            role_names = ["Admin", "Vendor", "Customer", "Logistics"]

            try:
                for role in role_names:
                    Role.objects.get_or_create(name=role)
            except (OperationalError, ProgrammingError, ObjectDoesNotExist):
                # Handle case where DB is not migrated yet
                pass

        # Run after migrations
        post_migrate.connect(create_roles, sender=self)
