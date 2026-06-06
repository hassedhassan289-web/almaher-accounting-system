# -*- coding: utf-8 -*-
"""
تطبيق نظام الماهر المحاسبي
النقطة الرئيسية للتطبيق
"""

import sys
from PyQt6.QtWidgets import QApplication
from config import APP_NAME, APP_VERSION
from ui.main_window import MainWindow

def main():
    """البرنامج الرئيسي"""
    app = QApplication(sys.argv)
    
    # تعيين معلومات التطبيق
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    # إنشاء وعرض النافذة الرئيسية
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
