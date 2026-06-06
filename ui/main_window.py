# -*- coding: utf-8 -*-
"""
النافذة الرئيسية للتطبيق
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QLabel, QStatusBar
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from config import APP_NAME, APP_VERSION, UI_WINDOW_WIDTH, UI_WINDOW_HEIGHT
from ui.sales import SalesWindow
from ui.purchases import PurchasesWindow
from ui.inventory import InventoryWindow
from ui.accounts import AccountsWindow
from ui.debts import DebtsWindow
from ui.reports import ReportsWindow

class MainWindow(QMainWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, UI_WINDOW_WIDTH, UI_WINDOW_HEIGHT)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # إنشاء الواجهة
        self.init_ui()
        
        # إظهار الحالة
        self.statusBar().showMessage("جاهز للعمل ✅")
    
    def init_ui(self):
        """تهيئة الواجهة الرئيسية"""
        
        # إنشاء الشريط العلوي
        self.create_toolbar()
        
        # إنشاء علامات التبويب
        self.create_tabs()
        
        # إنشاء شريط الحالة
        self.create_status_bar()
    
    def create_toolbar(self):
        """إنشاء شريط الأدوات العلوي"""
        toolbar = self.addToolBar("أدوات رئيسية")
        toolbar.setMovable(False)
        
        # زر المبيعات
        sales_btn = QPushButton("💳 المبيعات")
        sales_btn.setFixedSize(120, 40)
        sales_btn.clicked.connect(self.open_sales)
        toolbar.addWidget(sales_btn)
        
        # زر المشتريات
        purchases_btn = QPushButton("📦 المشتريات")
        purchases_btn.setFixedSize(120, 40)
        purchases_btn.clicked.connect(self.open_purchases)
        toolbar.addWidget(purchases_btn)
        
        # زر المخزون
        inventory_btn = QPushButton("📊 المخزون")
        inventory_btn.setFixedSize(120, 40)
        inventory_btn.clicked.connect(self.open_inventory)
        toolbar.addWidget(inventory_btn)
        
        # زر الصناديق
        accounts_btn = QPushButton("💰 الصناديق")
        accounts_btn.setFixedSize(120, 40)
        accounts_btn.clicked.connect(self.open_accounts)
        toolbar.addWidget(accounts_btn)
        
        # زر الديون
        debts_btn = QPushButton("📋 الديون")
        debts_btn.setFixedSize(120, 40)
        debts_btn.clicked.connect(self.open_debts)
        toolbar.addWidget(debts_btn)
        
        # زر التقارير
        reports_btn = QPushButton("📈 التقارير")
        reports_btn.setFixedSize(120, 40)
        reports_btn.clicked.connect(self.open_reports)
        toolbar.addWidget(reports_btn)
    
    def create_tabs(self):
        """إنشاء علامات التبويب"""
        tabs = QTabWidget()
        tabs.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # إضافة علامات التبويب
        tabs.addTab(QWidget(), "الرئيسية")
        
        self.setCentralWidget(tabs)
    
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        status = self.statusBar()
        status.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    def open_sales(self):
        """فتح نافذة المبيعات"""
        self.sales_window = SalesWindow()
        self.sales_window.show()
    
    def open_purchases(self):
        """فتح نافذة المشتريات"""
        self.purchases_window = PurchasesWindow()
        self.purchases_window.show()
    
    def open_inventory(self):
        """فتح نافذة المخزون"""
        self.inventory_window = InventoryWindow()
        self.inventory_window.show()
    
    def open_accounts(self):
        """فتح نافذة الصناديق"""
        self.accounts_window = AccountsWindow()
        self.accounts_window.show()
    
    def open_debts(self):
        """فتح نافذة الديون"""
        self.debts_window = DebtsWindow()
        self.debts_window.show()
    
    def open_reports(self):
        """فتح نافذة التقارير"""
        self.reports_window = ReportsWindow()
        self.reports_window.show()
