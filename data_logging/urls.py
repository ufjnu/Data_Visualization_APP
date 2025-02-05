from django.urls import path
from .views import get_logs, import_logs, export_logs, apply_logs

urlpatterns = [
    path("logs/", get_logs, name="get_logs"),
    path("logs/import/", import_logs, name="import_logs"),
    path("logs/export/", export_logs, name="export_logs"),
    path("logs/apply/", apply_logs, name="apply_logs"),
]