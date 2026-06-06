# -*- coding: utf-8 -*-
"""
نظام إدارة الديون والمديونية - فواتير آجلة وسداد العملاء
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QMessageBox, QHeaderView, QDateEdit, QTextEdit, QFormLayout,
    QDoubleSpinBox, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt, QDate
from database import db
from datetime import datetime

class DebtsWindow(QMainWindow):
    """نافذة إدارة الديون والمديونية"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💳 نظام إدارة الديون والمديونية")
        self.setGeometry(100, 100, 1400, 800)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        tabs = QTabWidget()
        tabs.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # تبويب العملاء المديونين
        tabs.addTab(self.create_debtors_tab(), "👥 العملاء المديونين")
        
        # تبويب سند السداد
        tabs.addTab(self.create_payment_receipt_tab(), "📄 سند قبض الدين")
        
        # تبويب تجديد الفواتير الآجلة
        tabs.addTab(self.create_credit_invoices_tab(), "📋 الفواتير الآجلة")
        
        # تبويب تقارير الديون
        tabs.addTab(self.create_debt_reports_tab(), "📊 تقارير الديون")
        
        # تبويب سجل السدادات
        tabs.addTab(self.create_payments_log_tab(), "📜 سجل السدادات")
        
        self.setCentralWidget(tabs)
    
    def create_debtors_tab(self):
        """تبويب العملاء المديونين"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("👥 قائمة العملاء المديونين")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # فلاتر البحث
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("🔍 بحث:"))
        search_input = QLineEdit()
        search_input.setPlaceholderText("ابحث باسم العميل أو الرقم...")
        filter_layout.addWidget(search_input)
        
        status_combo = QComboBox()
        status_combo.addItems(["الكل", "ديون نشطة", "ديون متأخرة", "مسددة"])
        filter_layout.addWidget(status_combo)
        
        search_btn = QPushButton("🔍 بحث")
        filter_layout.addWidget(search_btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # جدول العملاء المديونين
        self.debtors_table = QTableWidget()
        self.debtors_table.setColumnCount(7)
        self.debtors_table.setHorizontalHeaderLabels([
            "كود العميل", "الاسم", "الهاتف", "الدين الكلي", "المدفوع", "المتبقي", "الحالة"
        ])
        self.debtors_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.debtors_table)
        
        # ملخص الديون
        summary_layout = QHBoxLayout()
        summary_layout.addWidget(QLabel("📊 إجمالي الديون:"))
        self.total_debt_label = QLabel("0.00 ريال")
        self.total_debt_label.setStyleSheet("font-weight: bold; color: red; font-size: 14px;")
        summary_layout.addWidget(self.total_debt_label)
        
        summary_layout.addWidget(QLabel("| عدد المديونين:"))
        self.debtors_count_label = QLabel("0")
        self.debtors_count_label.setStyleSheet("font-weight: bold; color: blue;")
        summary_layout.addWidget(self.debtors_count_label)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # تحديث البيانات
        self.refresh_debtors()
        
        widget.setLayout(layout)
        return widget
    
    def create_payment_receipt_tab(self):
        """تبويب سند قبض الدين"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📄 سند قبض الدين - إدارة السدادات")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: blue;")
        layout.addWidget(title)
        
        # بيانات السند
        form = QFormLayout()
        
        # اختيار العميل
        customer_combo = QComboBox()
        customer_combo.addItem("-- اختر العميل --")
        form.addRow("العميل:", customer_combo)
        
        # الدين الحالي
        debt_info = QTextEdit()
        debt_info.setReadOnly(True)
        debt_info.setMaximumHeight(80)
        form.addRow("معلومات الدين:", debt_info)
        
        # المبلغ المسدد
        amount_spin = QDoubleSpinBox()
        amount_spin.setMaximum(9999999)
        form.addRow("المبلغ المسدد (ريال):", amount_spin)
        
        # طريقة الدفع
        payment_method = QComboBox()
        payment_method.addItems(["💵 نقدي", "🏦 تحويل بنكي", "💳 بطاقة ائتمان", "شيك"])
        form.addRow("طريقة الدفع:", payment_method)
        
        # ملاحظات
        notes = QTextEdit()
        notes.setMaximumHeight(100)
        form.addRow("ملاحظات:", notes)
        
        layout.addLayout(form)
        
        # المتبقي بعد السداد
        remaining_layout = QHBoxLayout()
        remaining_layout.addWidget(QLabel("المتبقي بعد السداد:"))
        remaining_label = QLabel("0.00 ريال")
        remaining_label.setStyleSheet("font-weight: bold; color: green; font-size: 14px;")
        remaining_layout.addWidget(remaining_label)
        remaining_layout.addStretch()
        layout.addLayout(remaining_layout)
        
        # أزرار
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("🗑️ مسح")
        btn_layout.addWidget(clear_btn)
        
        save_btn = QPushButton("✅ حفظ السند")
        save_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        btn_layout.addWidget(save_btn)
        
        print_btn = QPushButton("🖨️ طباعة السند")
        btn_layout.addWidget(print_btn)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_credit_invoices_tab(self):
        """تبويب الفواتير الآجلة"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📋 إدارة الفواتير الآجلة")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # فلاتر البحث
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("🔍 من:"))
        filter_layout.addWidget(QDateEdit())
        filter_layout.addWidget(QLabel("إلى:"))
        filter_layout.addWidget(QDateEdit())
        
        status_combo = QComboBox()
        status_combo.addItems(["الكل", "مسددة", "جزئية", "معلقة"])
        filter_layout.addWidget(status_combo)
        
        search_btn = QPushButton("🔍 بحث")
        filter_layout.addWidget(search_btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # جدول الفواتير الآجلة
        self.credit_invoices_table = QTableWidget()
        self.credit_invoices_table.setColumnCount(8)
        self.credit_invoices_table.setHorizontalHeaderLabels([
            "رقم الفاتورة", "التاريخ", "العميل", "الإجمالي", "المدفوع", "المتبقي", "الحالة", "الإجراءات"
        ])
        self.credit_invoices_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.credit_invoices_table)
        
        # إحصائيات
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(QLabel("📊 إجمالي الفواتير الآجلة:"))
        stats_label = QLabel("0 | المبلغ: 0.00 ريال")
        stats_label.setStyleSheet("font-weight: bold; color: blue;")
        stats_layout.addWidget(stats_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_debt_reports_tab(self):
        """تبويب تقارير الديون"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📊 تقارير الديون المتقدمة")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: blue;")
        layout.addWidget(title)
        
        # اختيار نوع التقرير
        report_layout = QHBoxLayout()
        report_layout.addWidget(QLabel("نوع التقرير:"))
        report_type = QComboBox()
        report_type.addItems([
            "🔴 الديون المتأخرة (أكثر من 30 يوم)",
            "🟠 الديون المتأخرة (أكثر من 60 يوم)",
            "🟡 الديون القريبة للاستحقاق (قبل 7 أيام)",
            "💚 الديون المسددة بالكامل",
            "📊 تحليل الديون حسب الفترة الزمنية"
        ])
        report_layout.addWidget(report_type)
        report_layout.addStretch()
        layout.addLayout(report_layout)
        
        # التقرير
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)
        
        # الرسوم البيانية
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels(["العميل", "الدين", "المدفوع", "النسبة"])
        layout.addWidget(self.report_table)
        
        # أزرار
        btn_layout = QHBoxLayout()
        generate_btn = QPushButton("📊 توليد التقرير")
        generate_btn.setStyleSheet("background-color: blue; color: white;")
        btn_layout.addWidget(generate_btn)
        
        export_btn = QPushButton("📥 تصدير PDF")
        btn_layout.addWidget(export_btn)
        
        print_btn = QPushButton("🖨️ طباعة")
        btn_layout.addWidget(print_btn)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_payments_log_tab(self):
        """تبويب سجل السدادات"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📜 سجل جميع السدادات")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # فلاتر البحث
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("من:"))
        filter_layout.addWidget(QDateEdit())
        filter_layout.addWidget(QLabel("إلى:"))
        filter_layout.addWidget(QDateEdit())
        filter_layout.addWidget(QPushButton("🔍 بحث"))
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # جدول السدادات
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(7)
        self.payments_table.setHorizontalHeaderLabels([
            "التاريخ والوقت", "العميل", "رقم الفاتورة", "المبلغ المسدد", "طريقة الدفع", "المتبقي", "الملاحظات"
        ])
        self.payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.payments_table)
        
        # الإحصائيات
        stats_label = QLabel("📊 إجمالي السدادات: 0.00 ريال | عدد السندات: 0")
        stats_label.setStyleSheet("font-weight: bold; color: green;")
        layout.addWidget(stats_label)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_debtors(self):
        """تحديث قائمة العملاء المديونين"""
        debtors = db.fetchall('SELECT * FROM customers WHERE total_debt > 0 ORDER BY total_debt DESC')
        self.debtors_table.setRowCount(len(debtors))
        
        total_debt = 0
        for row, debtor in enumerate(debtors):
            self.debtors_table.setItem(row, 0, QTableWidgetItem(str(debtor['id'])))
            self.debtors_table.setItem(row, 1, QTableWidgetItem(debtor['customer_name']))
            self.debtors_table.setItem(row, 2, QTableWidgetItem(debtor['phone'] or "-"))
            self.debtors_table.setItem(row, 3, QTableWidgetItem(f"{debtor['total_debt']:,.2f}"))
            
            # محسوب من الفواتير
            paid = db.fetchone(
                'SELECT SUM(paid_amount) as total FROM sales_invoices WHERE customer_id = ?',
                (debtor['id'],)
            )
            paid_amount = paid['total'] or 0
            
            remaining = debtor['total_debt'] - paid_amount
            self.debtors_table.setItem(row, 4, QTableWidgetItem(f"{paid_amount:,.2f}"))
            self.debtors_table.setItem(row, 5, QTableWidgetItem(f"{remaining:,.2f}"))
            
            # الحالة
            status = "متأخر" if remaining > 0 else "مسدد"
            self.debtors_table.setItem(row, 6, QTableWidgetItem(status))
            
            total_debt += debtor['total_debt']
        
        self.total_debt_label.setText(f"{total_debt:,.2f} ريال")
        self.debtors_count_label.setText(str(len(debtors)))

