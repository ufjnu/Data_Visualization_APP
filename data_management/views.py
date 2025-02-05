from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset
from .serializers import DatasetSerializer
import pandas as pd
import json


# DatasetUploadView: 接收文件上传并存储。
# DatasetRetrieveView: 根据 dataset_id 返回原始数据。
# DatasetSaveChangesView: 接收并存储数据的更改部分。
# DatasetDownloadView: 返回应用所有日志操作后的最终数据。
# 辅助函数 (utils.py)：提供应用日志到数据集的逻辑。
# API 路由 (urls.py)：定义了数据上传、读取、保存更改、下载的接口。

class DatasetUploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.create(name=file.name, original_file=file)
        return Response(DatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)

class DatasetRetrieveView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)

        # Read the original file
        data = pd.read_csv(dataset.original_file.path)
        return Response({"data": data.to_dict(orient="records")})

class DatasetSaveChangesView(APIView):
    def post(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)

        # Get changes as JSON
        changes = request.data.get("changes", [])
        if not changes:
            return Response({"error": "No changes provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Apply changes to the dataset
        original_data = pd.read_csv(dataset.original_file.path)
        for change in changes:
            # Example: Apply changes (logic depends on the format of 'changes')
            pass

        # Save updated dataset to a new file
        updated_file_path = f"datasets/updated/{dataset.name}_updated.csv"
        original_data.to_csv(updated_file_path, index=False)
        return JsonResponse({"status": "Changes saved", "updated_file": updated_file_path})

class DatasetDownloadView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        original_data = pd.read_csv(dataset.original_file.path)

        # Apply logs from the data_logging app (pseudo-code)
        logs = []  # Fetch logs for this dataset
        for log in logs:
            pass  # Apply log to original_data

        # Convert to downloadable response
        response = JsonResponse(original_data.to_dict(orient="records"))
        response["Content-Disposition"] = f"attachment; filename={dataset.name}_final.csv"
        return response

