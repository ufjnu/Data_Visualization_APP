from django.urls import path
from .views import DatasetUploadView, DatasetRetrieveView, DatasetSaveChangesView, DatasetDownloadView

urlpatterns = [
    path('upload/', DatasetUploadView.as_view(), name='dataset_upload'),
    path('<int:dataset_id>/', DatasetRetrieveView.as_view(), name='dataset_retrieve'),
    path('<int:dataset_id>/save_changes/', DatasetSaveChangesView.as_view(), name='dataset_save_changes'),
    path('<int:dataset_id>/download/', DatasetDownloadView.as_view(), name='dataset_download'),
]