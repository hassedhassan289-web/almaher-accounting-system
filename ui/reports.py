# -*- coding: utf-8 -*-
"""
نافذة التقارير والبيانات
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ReportsWindow(QMainWindow):
    """نافذة التقارير والبيانات"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 التقارير والبيانات")
        self.setGeometry(200, 200, 1000, 700)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # إنشاء الواجهة
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("نافذة التقارير والبيانات")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
