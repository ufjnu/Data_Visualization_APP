from django.apps import AppConfig


def reset_db_after_migrate(sender, **kwargs):
    class DataManagementConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'data_management'

