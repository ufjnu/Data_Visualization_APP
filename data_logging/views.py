from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LogEntry
import json
import os

#get_logs: 返回日志列表，供前端显示。
# import_logs: 导入日志文件并存储到数据库。
# export_logs: 导出日志文件供下载。
# apply_logs: 执行日志操作，更新数据集。

@csrf_exempt
def get_logs(request):
    if request.method == "GET":
        logs = LogEntry.objects.all().values("timestamp", "action")
        return JsonResponse({"logs": list(logs)})

@csrf_exempt
def import_logs(request):
    if request.method == "POST":
        try:
            uploaded_file = request.FILES.get("file")
            if not uploaded_file:
                return JsonResponse({"error": "No file provided."}, status=400)

            logs = json.load(uploaded_file)
            for log in logs:
                LogEntry.objects.create(timestamp=log["timestamp"], action=log["action"])

            return JsonResponse({"logs": list(LogEntry.objects.all().values("timestamp", "action"))})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def export_logs(request):
    if request.method == "GET":
        logs = list(LogEntry.objects.all().values("timestamp", "action"))
        response = JsonResponse(logs, safe=False)
        response["Content-Disposition"] = "attachment; filename=logs.json"
        return response

@csrf_exempt
def apply_logs(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logs = data.get("logs", [])

            # Here you would apply the logs to the current dataset
            updated_dataset = []  # Placeholder for updated dataset

            return JsonResponse({"updatedDataset": updated_dataset})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)