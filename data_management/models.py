from django.db import models

# Create your models here. 数据管理保存 1上传的原始数据表2每一步的日志（在log保存）3临时数据库
from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    original_file = models.FileField(upload_to='datasets/originals/')  # Stores the original dataset
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name