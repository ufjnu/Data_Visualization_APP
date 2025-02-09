#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import shutil
from django.core.management import call_command
from django.conf import settings

def main():

    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")

    # 🚀 仅在 `runserver` 时执行清空数据库 + 迁移
    if "runserver" in sys.argv:
        print("⚠️ 自动重建数据库 & 清空 `media/` 目录...")

        # 1️⃣ 删除 SQLite 数据库文件（如果用的是 SQLite）
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

        # 3️⃣ 重新迁移数据库
        #print("🚀 重新迁移数据库...")
        #call_command("migrate")



    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
