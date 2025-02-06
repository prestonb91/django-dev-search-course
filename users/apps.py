from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Allows this app to know about user signals since separated from model. 
    def ready(self):
            import users.signals