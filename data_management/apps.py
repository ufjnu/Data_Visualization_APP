from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command
import shutil
import os
from django.conf import settings

def reset_db_after_migrate(sender, **kwargs):
    """每次 `migrate` 之后，自动删除数据库 & 重新迁移"""
    print("⚠️ 迁移后自动清空数据库 & `media/` 目录...")

    # 1️⃣ 删除 SQLite 数据库（如果用的是 SQLite）
    #db_path = settings.DATABASES.get("default", {}).get("NAME")
    #if db_path and os.path.exists(db_path):
        #print(f"🗑️ 删除数据库文件: {db_path}")
        #os.remove(db_path)

    # 2️⃣ 清空 `media/` 目录
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        print("🗑️ 清空 `media/` 目录...")
        shutil.rmtree(media_root)
        os.makedirs(media_root, exist_ok=True)

    # 3️⃣ 重新运行 `migrate`
    #print("🚀 重新迁移数据库...")
    #call_command("migrate")

class DataManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_management'

    def ready(self):
        post_migrate.connect(reset_db_after_migrate, sender=self)
