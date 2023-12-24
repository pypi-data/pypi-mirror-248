from django.apps import AppConfig


class RestFrameworkAdminConfig(AppConfig):
    name = 'rest_framework_admin'
    verbose_name = "Django REST framework Admin"

    # def ready(self):
    #     # Add System checks
    #     from .checks import pagination_system_check  # NOQA
