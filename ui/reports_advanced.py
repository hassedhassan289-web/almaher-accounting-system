# -*- coding: utf-8 -*-
"""
نظام التقارير الشاملة - صافي الأرباح والخسائر وتقارير الصناديق
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QHeaderView, QDateEdit, QTextEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from database import db
from datetime import datetime, timedelta

class ReportsWindow(QMainWindow):
    """نافذة التقارير الشاملة"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 نظام التقارير الشاملة")
        self.setGeometry(100, 100, 1600, 900)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        tabs = QTabWidget()
        tabs.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # تبويب الأرباح والخسائر
        tabs.addTab(self.create_profit_loss_tab(), "💹 الأرباح والخسائر")
        
        # تبويب جرد الصناديق
        tabs.addTab(self.create_cashbox_report_tab(), "💰 جرد الصناديق")
        
        # تبويب تتبع IMEI
        tabs.addTab(self.create_imei_trace_tab(), "📱 تتبع IMEI")
        
        # تبويب ميزان المراجعة
        tabs.addTab(self.create_trial_balance_tab(), "📋 ميزان المراجعة")
        
        # تبويب المخزون
        tabs.addTab(self.create_inventory_report_tab(), "📦 تقرير المخزون")
        
        self.setCentralWidget(tabs)
    
    def create_profit_loss_tab(self):
        """تبويب تقرير الأرباح والخسائر"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("💹 تقرير صافي الأرباح والخسائر")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: blue;")
        layout.addWidget(title)
        
        # اختيار الفترة الزمنية
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("من:"))
        from_date = QDateEdit()
        from_date.setDate(QDate.currentDate().addMonths(-1))
        period_layout.addWidget(from_date)
        
        period_layout.addWidget(QLabel("إلى:"))
        to_date = QDateEdit()
        to_date.setDate(QDate.currentDate())
        period_layout.addWidget(to_date)
        
        period_combo = QComboBox()
        period_combo.addItems(["تخصيص", "هذا الشهر", "الشهر الماضي", "هذا الربع", "هذه السنة"])
        period_layout.addWidget(period_combo)
        
        generate_btn = QPushButton("📊 توليد التقرير")
        generate_btn.setStyleSheet("background-color: blue; color: white;")
        generate_btn.clicked.connect(self.generate_profit_loss)
        period_layout.addWidget(generate_btn)
        period_layout.addStretch()
        layout.addLayout(period_layout)
        
        # التقرير الرئيسي
        self.profit_loss_report = QTextEdit()
        self.profit_loss_report.setReadOnly(True)
        self.profit_loss_report.setStyleSheet("font-family: Courier; font-size: 11px;")
        layout.addWidget(self.profit_loss_report)
        
        # جدول التفاصيل
        self.profit_table = QTableWidget()
        self.profit_table.setColumnCount(5)
        self.profit_table.setHorizontalHeaderLabels(["البند", "المبلغ (ريال)", "النسبة %", "الملاحظات", ""])
        self.profit_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.profit_table)
        
        # الأزرار
        btn_layout = QHBoxLayout()
        export_btn = QPushButton("📥 تصدير Excel")
        btn_layout.addWidget(export_btn)
        
        pdf_btn = QPushButton("📥 تصدير PDF")
        btn_layout.addWidget(pdf_btn)
        
        print_btn = QPushButton("🖨️ طباعة")
        btn_layout.addWidget(print_btn)
        
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget
    
    def create_cashbox_report_tab(self):
        """تبويب جرد الصناديق"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("💰 تقرير جرد الصناديق - نهاية اليوم")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
        layout.addWidget(title)
        
        # التاريخ
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("التاريخ:"))
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_edit)
        
        generate_btn = QPushButton("📊 توليد الجرد")
        generate_btn.setStyleSheet("background-color: green; color: white;")
        generate_btn.clicked.connect(self.generate_cashbox_report)
        date_layout.addWidget(generate_btn)
        date_layout.addStretch()
        layout.addLayout(date_layout)
        
        # ملخص الحركات
        summary_label = QLabel("📋 ملخص حركات اليوم:")
        summary_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(summary_label)
        
        self.cashbox_summary = QTextEdit()
        self.cashbox_summary.setReadOnly(True)
        self.cashbox_summary.setMaximumHeight(120)
        layout.addWidget(self.cashbox_summary)
        
        # جدول التفاصيل
        detail_label = QLabel("📊 تفاصيل الحركات:")
        detail_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(detail_label)
        
        self.cashbox_table = QTableWidget()
        self.cashbox_table.setColumnCount(6)
        self.cashbox_table.setHorizontalHeaderLabels([
            "الوقت", "نوع الحركة", "الصندوق", "المبلغ", "الرصيد", "الملاحظات"
        ])
        self.cashbox_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.cashbox_table)
        
        # الفائض أو العجز
        diff_layout = QHBoxLayout()
        diff_layout.addWidget(QLabel("الفائض/العجز:"))
        self.diff_label = QLabel("0.00 ريال")
        self.diff_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        diff_layout.addWidget(self.diff_label)
        diff_layout.addStretch()
        layout.addLayout(diff_layout)
        
        # الأزرار
        btn_layout = QHBoxLayout()
        export_btn = QPushButton("📥 تصدير PDF")
        btn_layout.addWidget(export_btn)
        
        print_btn = QPushButton("🖨️ طباعة")
        btn_layout.addWidget(print_btn)
        
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget
    
    def create_imei_trace_tab(self):
        """تبويب تتبع IMEI"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📱 تتبع الهواتف الذكية حسب IMEI")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # البحث
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 IMEI:"))
        imei_input = QLineEdit()
        imei_input.setPlaceholderText("أدخل رقم IMEI...")
        search_layout.addWidget(imei_input)
        
        search_btn = QPushButton("بحث")
        search_layout.addWidget(search_btn)
        search_layout.addStretch()
        layout.addLayout(search_layout)
        
        # معلومات الجهاز
        info_label = QLabel("📋 معلومات الجهاز:")
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)
        
        device_info = QTextEdit()
        device_info.setReadOnly(True)
        device_info.setMaximumHeight(100)
        layout.addWidget(device_info)
        
        # سجل الحركات
        history_label = QLabel("📜 سجل حركات الجهاز:")
        history_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(history_label)
        
        self.imei_table = QTableWidget()
        self.imei_table.setColumnCount(7)
        self.imei_table.setHorizontalHeaderLabels([
            "التاريخ", "نوع الحركة", "الطرف", "السعر", "الحالة", "ملاحظات", "الضمان"
        ])
        self.imei_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.imei_table)
        
        widget.setLayout(layout)
        return widget
    
    def create_trial_balance_tab(self):
        """تبويب ميزان المراجعة"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📋 ميزان المراجعة والميزانية")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: purple;")
        layout.addWidget(title)
        
        # التاريخ
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("حتى:"))
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_edit)
        
        generate_btn = QPushButton("📊 توليد الميزان")
        generate_btn.setStyleSheet("background-color: purple; color: white;")
        btn_layout.addWidget(generate_btn)
        date_layout.addStretch()
        layout.addLayout(date_layout)
        
        # جدول الميزان
        self.trial_table = QTableWidget()
        self.trial_table.setColumnCount(4)
        self.trial_table.setHorizontalHeaderLabels([
            "الحساب", "الرصيد المدين", "الرصيد الدائن", "الملاحظات"
        ])
        self.trial_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.trial_table)
        
        # الإجماليات
        totals_layout = QHBoxLayout()
        totals_layout.addWidget(QLabel("مجموع المدين:"))
        debit_label = QLabel("0.00")
        debit_label.setStyleSheet("font-weight: bold;")
        totals_layout.addWidget(debit_label)
        
        totals_layout.addWidget(QLabel("| مجموع الدائن:"))
        credit_label = QLabel("0.00")
        credit_label.setStyleSheet("font-weight: bold;")
        totals_layout.addWidget(credit_label)
        
        totals_layout.addStretch()
        layout.addLayout(totals_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_inventory_report_tab(self):
        """تبويب تقرير المخزون"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان
        title = QLabel("📦 تقرير المخزون والقيمة")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: brown;")
        layout.addWidget(title)
        
        # الفلاتر
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("الفئة:"))
        
        category_combo = QComboBox()
        category_combo.addItems(["الكل", "هواتف ذكية", "إكسسوارات", "قطع غيار"])
        filter_layout.addWidget(category_combo)
        
        generate_btn = QPushButton("📊 توليد التقرير")
        generate_btn.setStyleSheet("background-color: brown; color: white;")
        filter_layout.addWidget(generate_btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # جدول المخزون
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(8)
        self.inventory_table.setHorizontalHeaderLabels([
            "كود", "الاسم", "الفئة", "الكمية", "سعر التكلفة", "القيمة الإجمالية", "حد الطلب", "الحالة"
        ])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.inventory_table)
        
        # ملخص المخزون
        summary_layout = QHBoxLayout()
        summary_layout.addWidget(QLabel("📊 قيمة المخزون الإجمالية:"))
        total_value = QLabel("0.00 ريال")
        total_value.setStyleSheet("font-weight: bold; color: green; font-size: 14px;")
        summary_layout.addWidget(total_value)
        
        summary_layout.addWidget(QLabel("| الأصناف الناقصة:"))
        low_count = QLabel("0")
        low_count.setStyleSheet("font-weight: bold; color: red;")
        summary_layout.addWidget(low_count)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        widget.setLayout(layout)
        return widget
    
    # ==================== دوال التقارير ====================
    
    def generate_profit_loss(self):
        """توليد تقرير الأرباح والخسائر"""
        try:
            # جلب المبيعات
            sales = db.fetchone(
                'SELECT SUM(total_amount) as total FROM sales_invoices WHERE invoice_date >= ?',
                (datetime.now().strftime('%Y-%m-01'),)
            )
            total_sales = sales['total'] or 0
            
            # جلب المشتريات
            purchases = db.fetchone(
                'SELECT SUM(total_amount) as total FROM purchase_invoices WHERE invoice_date >= ?',
                (datetime.now().strftime('%Y-%m-01'),)
            )
            total_purchases = purchases['total'] or 0
            
            # الأرباح
            profit = total_sales - total_purchases
            profit_margin = (profit / total_sales * 100) if total_sales > 0 else 0
            
            # عرض التقرير
            report_text = f"""
╔════════════════════════════════════════════════════════════════╗
║            تقرير الأرباح والخسائر الشهري                        ║
╚════════════════════════════════════════════════════════════════╝

📈 المبيعات الإجمالية:          {total_sales:>30,.2f} ريال
📦 تكلفة المشتريات:             {total_purchases:>30,.2f} ريال
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💹 صافي الأرباح:                {profit:>30,.2f} ريال
📊 نسبة الربح:                  {profit_margin:>29,.2f}%
            """
            
            self.profit_loss_report.setText(report_text)
            QMessageBox.information(self, "نجاح", "تم توليد التقرير بنجاح!")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في توليد التقرير: {str(e)}")
    
    def generate_cashbox_report(self):
        """توليد تقرير جرد الصناديق"""
        try:
            accounts = db.fetchall('SELECT * FROM accounts')
            total_balance = sum(acc['balance_yer'] for acc in accounts)
            
            summary = f"""
╔════════════════════════════════════════════════════════════════╗
║              جرد الصناديق - نهاية اليوم                        ║
║              التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╚════════════════════════════════════════════════════════════════╝

"""
            for acc in accounts:
                summary += f"{acc['account_name']:<40} {acc['balance_yer']:>15,.2f} ريال\n"
            
            summary += f"\n{'━' * 60}\n"
            summary += f"{'الإجمالي الكلي':<40} {total_balance:>15,.2f} ريال\n"
            
            self.cashbox_summary.setText(summary)
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في توليد الجرد: {str(e)}")

from PyQt6.QtWidgets import QLineEdit

