from django.apps import AppConfig


class RmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rm_app'
    def ready(self):
        import rm_app.signals