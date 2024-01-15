from django.apps import AppConfig

class AuthSetupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_setup'

    def ready(self):
        import auth_setup.signals
