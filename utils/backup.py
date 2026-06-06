# -*- coding: utf-8 -*-
"""
أداة النسخ الاحتياطي والاستعادة
"""

import os
import shutil
from datetime import datetime
from config import DB_PATH, BACKUP_DIR, BACKUP_RETENTION_DAYS

class BackupManager:
    """مدير النسخ الاحتياطي"""
    
    @staticmethod
    def create_backup():
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            # إنشاء مسار النسخة الاحتياطية
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = f"AlMaher_Backup_{timestamp}.db"
            backup_path = os.path.join(BACKUP_DIR, backup_filename)
            
            # نسخ ملف قاعدة البيانات
            if os.path.exists(DB_PATH):
                shutil.copy2(DB_PATH, backup_path)
                print(f"✅ تم إنشاء نسخة احتياطية: {backup_filename}")
                return True, backup_path
        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False, str(e)
    
    @staticmethod
    def restore_backup(backup_filename):
        """استعادة من نسخة احتياطية"""
        try:
            backup_path = os.path.join(BACKUP_DIR, backup_filename)
            
            if not os.path.exists(backup_path):
                return False, "النسخة الاحتياطية غير موجودة"
            
            # نسخ النسخة الاحتياطية إلى مسار قاعدة البيانات الحالي
            shutil.copy2(backup_path, DB_PATH)
            print(f"✅ تمت استعادة قاعدة البيانات من: {backup_filename}")
            return True, "تمت الاستعادة بنجاح"
        except Exception as e:
            print(f"❌ خطأ في استعادة النسخة الاحتياطية: {e}")
            return False, str(e)
    
    @staticmethod
    def list_backups():
        """قائمة بجميع النسخ الاحتياطية المتاحة"""
        try:
            backups = []
            if os.path.exists(BACKUP_DIR):
                for filename in sorted(os.listdir(BACKUP_DIR), reverse=True):
                    filepath = os.path.join(BACKUP_DIR, filename)
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                        backups.append({
                            "filename": filename,
                            "size": size,
                            "modified": modified_time.strftime("%Y-%m-%d %H:%M:%S")
                        })
            return backups
        except Exception as e:
            print(f"❌ خطأ في جلب قائمة النسخ الاحتياطية: {e}")
            return []
    
    @staticmethod
    def cleanup_old_backups():
        """حذف النسخ الاحتياطية القديمة"""
        try:
            import datetime as dt
            cutoff_date = dt.datetime.now() - dt.timedelta(days=BACKUP_RETENTION_DAYS)
            
            if os.path.exists(BACKUP_DIR):
                for filename in os.listdir(BACKUP_DIR):
                    filepath = os.path.join(BACKUP_DIR, filename)
                    if os.path.isfile(filepath):
                        file_modified = dt.datetime.fromtimestamp(os.path.getmtime(filepath))
                        if file_modified < cutoff_date:
                            os.remove(filepath)
                            print(f"🗑️ تم حذف النسخة القديمة: {filename}")
        except Exception as e:
            print(f"❌ خطأ في حذف النسخ الاحتياطية القديمة: {e}")
