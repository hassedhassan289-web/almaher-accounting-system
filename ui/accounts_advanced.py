# -*- coding: utf-8 -*-
"""
نظام إدارة الصناديق والحسابات - صندوق الكاشير والخزنة والتحويلات المالية
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QMessageBox, QHeaderView, QDateEdit, QTextEdit, QFormLayout,
    QDoubleSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, QDate
from database import db
from datetime import datetime

class AccountsWindow(QMainWindow):
    """نافذة إدارة الصناديق والحسابات"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💰 نظام إدارة الصناديق والحسابات")
        self.setGeometry(100, 100, 1400, 800)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        tabs = QTabWidget()
        tabs.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # تبويب الصناديق
        tabs.addTab(self.create_accounts_tab(), "📦 الصناديق")
        
        # تبويب التحويلات
        tabs.addTab(self.create_transfers_tab(), "↔️ التحويلات المالية")
        
        # تبويب السحب والإيداع
        tabs.addTab(self.create_deposits_withdrawals_tab(), "💸 السحب والإيداع")
        
        # تبويب جرد الوردية
        tabs.addTab(self.create_shift_closing_tab(), "📊 جرد الوردية")
        
        # تبويب السجل
        tabs.addTab(self.create_transactions_log_tab(), "📜 سجل الحركات")
        
        self.setCentralWidget(tabs)
    
    def create_accounts_tab(self):
        """تبويب الصناديق والحسابات"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("🏦 الصناديق والحسابات")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # جدول الصناديق
        self.accounts_table = QTableWidget()
        self.accounts_table.setColumnCount(4)
        self.accounts_table.setHorizontalHeaderLabels(["اسم الصندوق", "الرصيد الحالي (ريال)", "آخر تحديث", "العمليات"])
        self.accounts_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.accounts_table)
        
        # تحديث البيانات
        self.refresh_accounts()
        
        # ملخص إجمالي
        summary_layout = QHBoxLayout()
        summary_layout.addWidget(QLabel("💵 إجمالي الأموال في الصناديق:"))
        self.total_balance = QLabel("0.00 ريال")
        self.total_balance.setStyleSheet("font-weight: bold; color: green; font-size: 16px;")
        summary_layout.addWidget(self.total_balance)
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # أزرار التحديث
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.clicked.connect(self.refresh_accounts)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_transfers_tab(self):
        """تبويب التحويلات المالية بين الصناديق"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("↔️ تحويل أموال بين الصناديق")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # نموذج التحويل
        form = QFormLayout()
        
        # من صندوق
        from_combo = QComboBox()
        from_combo.addItem("صندوق النقدية الكاشير")
        from_combo.addItem("الخزنة الرئيسية")
        from_combo.addItem("صندوق المديونية")
        form.addRow("من صندوق:", from_combo)
        
        # إلى صندوق
        to_combo = QComboBox()
        to_combo.addItem("الخزنة الرئيسية")
        to_combo.addItem("صندوق النقدية الكاشير")
        to_combo.addItem("صندوق المديونية")
        form.addRow("إلى صندوق:", to_combo)
        
        # المبلغ
        amount_spin = QDoubleSpinBox()
        amount_spin.setMaximum(9999999)
        form.addRow("المبلغ (ريال):", amount_spin)
        
        # السبب/الملاحظات
        reason_input = QTextEdit()
        reason_input.setMaximumHeight(100)
        form.addRow("السبب/الملاحظات:", reason_input)
        
        layout.addLayout(form)
        
        # أزرار
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("🗑️ مسح")
        btn_layout.addWidget(clear_btn)
        
        save_btn = QPushButton("✅ تنفيذ التحويل")
        save_btn.setStyleSheet("background-color: blue; color: white; font-weight: bold;")
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_deposits_withdrawals_tab(self):
        """تبويب السحب والإيداع"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # اختيار نوع العملية
        operation_layout = QHBoxLayout()
        operation_layout.addWidget(QLabel("نوع العملية:"))
        self.operation_type = QComboBox()
        self.operation_type.addItems(["💸 سحب", "💳 إيداع"])
        operation_layout.addWidget(self.operation_type)
        operation_layout.addStretch()
        layout.addLayout(operation_layout)
        
        # الصندوق
        form = QFormLayout()
        account_combo = QComboBox()
        account_combo.addItem("صندوق النقدية الكاشير")
        account_combo.addItem("الخزنة الرئيسية")
        form.addRow("الصندوق:", account_combo)
        
        # المبلغ
        amount_spin = QDoubleSpinBox()
        amount_spin.setMaximum(9999999)
        form.addRow("المبلغ (ريال):", amount_spin)
        
        # الملاحظات
        notes = QTextEdit()
        notes.setMaximumHeight(100)
        form.addRow("الملاحظات:", notes)
        
        layout.addLayout(form)
        
        # أزرار
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("🗑️ مسح"))
        confirm_btn = QPushButton("✅ تنفيذ")
        confirm_btn.setStyleSheet("background-color: green; color: white;")
        btn_layout.addWidget(confirm_btn)
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_shift_closing_tab(self):
        """تبويب جرد وتصفية الوردية"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📊 جرد وتصفية الوردية - تقرير نهاية اليوم")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: blue;")
        layout.addWidget(title)
        
        # التاريخ
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("التاريخ:"))
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_edit)
        date_layout.addStretch()
        layout.addLayout(date_layout)
        
        # ملخص الحركات
        summary_label = QLabel("📈 ملخص حركات اليوم:")
        summary_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(summary_label)
        
        self.closing_summary = QTextEdit()
        self.closing_summary.setReadOnly(True)
        self.closing_summary.setMaximumHeight(150)
        layout.addWidget(self.closing_summary)
        
        # جدول التفاصيل
        detail_label = QLabel("📋 تفاصيل الحركات:")
        detail_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(detail_label)
        
        self.closing_table = QTableWidget()
        self.closing_table.setColumnCount(5)
        self.closing_table.setHorizontalHeaderLabels(["الحركة", "الصندوق", "المبلغ", "الوقت", "الملاحظات"])
        layout.addWidget(self.closing_table)
        
        # الفائض أو العجز
        difference_layout = QHBoxLayout()
        difference_layout.addWidget(QLabel("الفائض/العجز:"))
        self.difference_label = QLabel("0.00 ريال")
        self.difference_label.setStyleSheet("font-weight: bold; font-size: 14px; color: red;")
        difference_layout.addWidget(self.difference_label)
        difference_layout.addStretch()
        layout.addLayout(difference_layout)
        
        # أزرار
        btn_layout = QHBoxLayout()
        generate_btn = QPushButton("📊 توليد التقرير")
        generate_btn.setStyleSheet("background-color: blue; color: white;")
        btn_layout.addWidget(generate_btn)
        
        export_btn = QPushButton("📥 تصدير PDF")
        btn_layout.addWidget(export_btn)
        
        close_shift_btn = QPushButton("✅ إغلاق الوردية")
        close_shift_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        btn_layout.addWidget(close_shift_btn)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_transactions_log_tab(self):
        """تبويب سجل الحركات المالية"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # الفلاتر
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("🔍 من:"))
        filter_layout.addWidget(QDateEdit())
        filter_layout.addWidget(QLabel("إلى:"))
        filter_layout.addWidget(QDateEdit())
        
        search_combo = QComboBox()
        search_combo.addItem("جميع الصناديق")
        search_combo.addItem("صندوق النقدية")
        search_combo.addItem("الخزنة")
        filter_layout.addWidget(search_combo)
        
        search_btn = QPushButton("🔍 بحث")
        filter_layout.addWidget(search_btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # جدول السجل
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(6)
        self.log_table.setHorizontalHeaderLabels(["التاريخ والوقت", "نوع الحركة", "من صندوق", "إلى صندوق", "المبلغ", "الملاحظات"])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.log_table)
        
        # الإحصائيات
        stats_label = QLabel("📊 إجمالي الحركات: 0 | إجمالي المبالغ: 0.00 ريال")
        stats_label.setStyleSheet("font-weight: bold; color: blue;")
        layout.addWidget(stats_label)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_accounts(self):
        """تحديث بيانات الصناديق"""
        accounts = db.fetchall('SELECT * FROM accounts')
        self.accounts_table.setRowCount(len(accounts))
        
        total = 0
        for row, account in enumerate(accounts):
            self.accounts_table.setItem(row, 0, QTableWidgetItem(account['account_name']))
            self.accounts_table.setItem(row, 1, QTableWidgetItem(f"{account['balance_yer']:,.2f}"))
            self.accounts_table.setItem(row, 2, QTableWidgetItem(account['created_at']))
            
            # زر معلومات
            info_btn = QPushButton("📋")
            self.accounts_table.setCellWidget(row, 3, info_btn)
            
            total += account['balance_yer']
        
        self.total_balance.setText(f"{total:,.2f} ريال")

