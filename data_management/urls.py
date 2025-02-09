from django.urls import path
from .views import (
    DatasetUploadView, DatasetRetrieveView, DatasetSaveChangesView,
    ReplicaCreateView, ReplicaDeleteView, ReplicaListView, ParsedDataView
)

urlpatterns = [
    path('upload/', DatasetUploadView.as_view(), name='dataset_upload'),
    path('<uuid:dataset_id>/', DatasetRetrieveView.as_view(), name='dataset_retrieve'),  # 改 int 为 uuid
    path('<uuid:dataset_id>/save_changes/', DatasetSaveChangesView.as_view(), name='dataset_save_changes'),
    #path('<uuid:dataset_id>/download/', DatasetDownloadView.as_view(), name='dataset_download'),

    # 🔹 新增副本管理 API
    path('<uuid:dataset_id>/replica/create/', ReplicaCreateView.as_view(), name='replica_create'),
    path('replica/<uuid:replica_id>/delete/', ReplicaDeleteView.as_view(), name='replica_delete'),
    path('<uuid:dataset_id>/replicas/', ReplicaListView.as_view(), name='replica_list'),  # **改为带 `dataset_id`**
    path('<uuid:dataset_id>/parsed/', ParsedDataView.as_view(), name='dataset_parsed'),  # 添加 `/parsed/`
]
