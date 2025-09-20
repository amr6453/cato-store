from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        # import signals
        from . import signals  # noqa: F401
    verbose_name = 'Orders'
