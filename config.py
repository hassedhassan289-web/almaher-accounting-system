# -*- coding: utf-8 -*-
"""
إعدادات نظام الماهر المحاسبي
"""

import os
from pathlib import Path

# المسارات الأساسية
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.path.join(BASE_DIR, "almaher_accounting.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# إعدادات التطبيق
APP_NAME = "نظام الماهر المحاسبي"
APP_VERSION = "1.0.0"
APP_AUTHOR = "حاشد"

# إعدادات قاعدة البيانات
DB_TIMEOUT = 30  # ثانية
DB_CHECK_SAME_THREAD = False

# إعدادات العملة
CURRENCY_NAME = "الريال اليمني"
CURRENCY_CODE = "YER"
CURRENCY_SYMBOL = "﷼"
CURRENCY_FRACTION = 1000  # 1000 فلس = 1 ريال

# أسعار الصرف الافتراضية (يمكن تحديثها من الواجهة)
EXCHANGE_RATES = {
    "YER": 1.0,
    "USD": 250.0,  # 1 دولار = 250 ريال (تقريبي)
    "SAR": 66.0,   # 1 سعودي = 66 ريال (تقريبي)
}

# إعدادات النسخ الاحتياطي
AUTO_BACKUP_ENABLED = True
AUTO_BACKUP_INTERVAL = 4 * 60 * 60  # 4 ساعات بالثواني
BACKUP_RETENTION_DAYS = 30  # احتفظ بالنسخ لمدة 30 يوم

# إعدادات الطباعة
PRINTER_WIDTH = 80  # عرض الطابعة الحرارية بـ ملم
PRINT_INVOICE_HEADER = True
PRINT_INVOICE_FOOTER = True

# إعدادات واجهة المستخدم
UI_THEME = "light"  # light أو dark
UI_LANGUAGE = "ar"  # عربي
UI_FONT_SIZE = 10
UI_WINDOW_WIDTH = 1200
UI_WINDOW_HEIGHT = 800

# إعدادات الأمان
MIN_STOCK_ALERT = 5  # عدد الأصناف قبل التنبيه
MAX_CUSTOMER_CREDIT = 500000  # الحد الأقصى للائتمان بالريال

# إعدادات التقارير
REPORT_DATE_FORMAT = "%Y-%m-%d"  # تنسيق التاريخ
REPORT_TIME_FORMAT = "%H:%M:%S"  # تنسيق الوقت

# الحسابات الافتراضية
DEFAULT_ACCOUNTS = {
    "CASH_BOX": "صندوق النقدية الكاشير",
    "DEBT_BOX": "صندوق مديونية العملاء",
    "MAIN_SAFE": "الخزنة الرئيسية",
    "PURCHASES": "حساب المشتريات",
    "SALES": "حساب المبيعات",
    "EXPENSES": "حساب المصروفات",
}

# فئات الأصناف
ITEM_CATEGORIES = {
    "phones": "هواتف ذكية",
    "accessories": "إكسسوارات",
    "spare_parts": "قطع غيار",
}

# أنواع الفواتير
INVOICE_TYPES = {
    "cash": "فاتورة نقدية",
    "credit": "فاتورة آجلة",
    "purchase": "فاتورة شراء",
}

# أنواع الحركات المالية
TRANSACTION_TYPES = {
    "sale": "بيع",
    "purchase": "شراء",
    "payment": "سداد",
    "transfer": "تحويل",
    "expense": "مصروف",
}
