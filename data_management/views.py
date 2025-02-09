from django.shortcuts import get_object_or_404
from django.conf import settings  # ✅ 确保 `settings.MEDIA_ROOT` 可用
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset, ParsedData, Replica
from .serializers import DatasetSerializer
import pandas as pd
import os


# ✅ 1. 修改 DatasetUploadView
class DatasetUploadView(APIView):
    """上传数据集并解析"""
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.create(name=file.name, original_file=file)
        print(f"✅ File saved: {dataset.original_file.path}")

        # **确保 `parsed/` 目录存在**
        parsed_dir = os.path.join(settings.MEDIA_ROOT, "datasets", "parsed")
        if not os.path.exists(parsed_dir):
            os.makedirs(parsed_dir)  # ✅ 自动创建目录
            print(f"📂 Created directory: {parsed_dir}")

        # 解析 CSV 并存储
        try:
            df = pd.read_csv(dataset.original_file.path)
            metadata = {"columns": list(df.columns), "num_rows": len(df)}

            parsed_file_path = os.path.join(parsed_dir, f"{dataset.id}.csv")
            df.to_csv(parsed_file_path, index=False)

            parsed_data = ParsedData.objects.create(dataset=dataset, parsed_file=parsed_file_path, metadata=metadata)
            return Response({
                "id": str(dataset.id),
                "name": dataset.name,
                "metadata": metadata
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            dataset.delete()  # 解析失败则删除文件
            return Response({"error": f"File parsing failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ 2. 修改 DatasetRetrieveView
class DatasetRetrieveView(APIView):
    """返回解析后的数据"""
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        parsed_data = get_object_or_404(ParsedData, dataset=dataset)

        return Response({"metadata": parsed_data.metadata})


# ✅ 3. 修改 DatasetSaveChangesView
class DatasetSaveChangesView(APIView):
    """存储修改后的数据"""
    def post(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        changes = request.data.get("changes", [])
        if not changes:
            return Response({"error": "No changes provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 读取原数据
        parsed_data = get_object_or_404(ParsedData, dataset=dataset)
        df = pd.read_csv(parsed_data.parsed_file.path)

        # 处理更改（假设 changes 是 JSON 形式）
        for change in changes:
            pass  # 这里应添加具体的处理逻辑

        updated_file_dir = os.path.join(settings.MEDIA_ROOT, "datasets", "updated")
        if not os.path.exists(updated_file_dir):
            os.makedirs(updated_file_dir)

        updated_file_path = os.path.join(updated_file_dir, f"{dataset.id}.csv")
        
        df.to_csv(updated_file_path, index=False)

        return Response({"message": "Changes saved", "updated_file": updated_file_path})


# ✅ 4. 新增 ReplicaCreateView
class ReplicaCreateView(APIView):
    """基于解析数据创建副本"""
    def post(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        parsed_data = get_object_or_404(ParsedData, dataset=dataset)

        new_name = request.data.get("new_name")
        if not new_name:
            return Response({"error": "No name provided"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 修正副本文件路径，避免 `media/media/`
        replicas_dir = os.path.join(settings.MEDIA_ROOT, "datasets", "replicas")
        if not os.path.exists(replicas_dir):
            os.makedirs(replicas_dir)  # **确保目录存在**

        replica_path = os.path.join(replicas_dir, f"{dataset.id}_{new_name}.csv")

        # 复制原解析数据
        df = pd.read_csv(parsed_data.parsed_file.path)
        df.to_csv(replica_path, index=False)

        # **存储副本信息**
        replica = Replica.objects.create(name=new_name, parsed_data=parsed_data, replica_file=replica_path)

        return Response({"id": str(replica.id), "name": replica.name}, status=status.HTTP_201_CREATED)


# ✅ 5. 新增 ReplicaDeleteView
class ReplicaDeleteView(APIView):
    """删除副本"""
    def delete(self, request, replica_id):
        replica = get_object_or_404(Replica, id=replica_id)
        replica.delete()
        return Response({"message": "Replica deleted"}, status=status.HTTP_204_NO_CONTENT)


# ✅ 6. 新增 ReplicaListView
class ReplicaListView(APIView):
    """获取某个数据集的所有副本"""
    def get(self, request, dataset_id):
        print(f"📌 Fetching replicas for dataset: {dataset_id}")  # ✅ 调试信息

        # ✅ 确保 `dataset_id` 存在于 `ParsedData`
        parsed_data = ParsedData.objects.filter(dataset__id=dataset_id).first()
        if not parsed_data:
            print("❌ Parsed data not found for dataset:", dataset_id)
            return Response({"error": "Parsed data not found"}, status=404)

        # ✅ 确保 `Replica` 存在
        replicas = Replica.objects.filter(parsed_data=parsed_data)
        if not replicas.exists():
            print("📌 No replicas found for dataset:", dataset_id)
            return Response({"replicas": []})  # ✅ 避免 404，而是返回空数组

        replica_list = [{
            "id": str(replica.id),
            "name": replica.name,
            "parent_id": str(replica.parent.id) if replica.parent else None,
            "metadata": replica.metadata
        } for replica in replicas]

        print(f"✅ Returning {len(replica_list)} replicas")
        return Response({"replicas": replica_list}, status=200)





class ParsedDataView(APIView):
    """返回解析数据的元数据"""

    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        parsed_data = ParsedData.objects.filter(dataset=dataset).first()

        if not parsed_data:
            return Response({"error": "Parsed data not found"}, status=404)

        return Response({
            "metadata": parsed_data.metadata
        })
