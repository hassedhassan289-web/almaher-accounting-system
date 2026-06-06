# -*- coding: utf-8 -*-
"""
نافذة إدارة الديون والمديونية
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class DebtsWindow(QMainWindow):
    """نافذة الديون والمديونية"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📋 إدارة الديون والمديونية")
        self.setGeometry(200, 200, 800, 600)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # إنشاء الواجهة
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("نافذة إدارة الديون والمديونية")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
