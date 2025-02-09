import uuid
from django.db import models

class Dataset(models.Model):
    """存储用户上传的原始 CSV 文件"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  # 文件名
    original_file = models.FileField(upload_to='datasets/originals/')  # 原始文件
    created_at = models.DateTimeField(auto_now_add=True)  # 上传时间

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class ParsedData(models.Model):
    """存储原文件解析后的数据"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name="parsed_data")  # 一对一关系
    parsed_file = models.FileField(upload_to='datasets/parsed/')  # 解析后的 CSV 文件
    metadata = models.JSONField(null=True, blank=True)  # 存储列名、行数等信息
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Parsed Data for {self.dataset.name}"


class Replica(models.Model):
    """存储副本，每个副本都是基于某个解析数据集的"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  # 副本名称

    parent = models.ForeignKey(
        'self',
        null=True,  # ✅ 允许 parent 为空
        blank=True,
        on_delete=models.SET_NULL,  # ✅ 删除父级副本时，不删除子副本，而是设为 NULL
        related_name="child_replicas"
    )

    parsed_data = models.ForeignKey(
        ParsedData,
        null=True,  # ✅ 允许 parsed_data 为空，避免 `on_delete=SET_NULL` 报错
        blank=True,
        on_delete=models.SET_NULL,  # ✅ 删除 `ParsedData` 时，不删除副本，只是 `parsed_data` 设为 NULL
        related_name="replicas"
    )

    replica_file = models.FileField(upload_to='datasets/replicas/', null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)  # 副本的列名等信息
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replica: {self.name} (Parent: {self.parent.name if self.parent else 'Original'})"



class ReplicaLog(models.Model):
    """记录副本的变更日志，如降维、清理数据等"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    replica = models.ForeignKey(Replica, on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=255)  # 例如 "Dimensionality Reduction (PCA)"
    parameters = models.JSONField(null=True, blank=True)  # 存储操作参数
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.replica.name}: {self.action} at {self.created_at}"
