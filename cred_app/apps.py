from django.apps import AppConfig


class CredAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cred_app'


class CredAppConfig(AppConfig):
    name = 'cred_app'

    def ready(self):
        import cred_app.signals  # Importe o módulo que contém os sinais  

