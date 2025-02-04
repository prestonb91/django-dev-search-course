from django.apps import AppConfig


# Connects with settings.py to indicate where models are and for migrate to work. 
class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'
