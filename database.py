# -*- coding: utf-8 -*-
"""
إدارة قاعدة البيانات - SQLite
"""

import sqlite3
import os
from datetime import datetime
from config import DB_PATH, DB_TIMEOUT, DEFAULT_ACCOUNTS, ITEM_CATEGORIES

class Database:
    """فئة إدارة قاعدة البيانات"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.conn = None
        self.init_database()
    
    def connect(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.conn = sqlite3.connect(self.db_path, timeout=DB_TIMEOUT, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"خطأ في الاتصال بقاعدة البيانات: {e}")
            return False
    
    def disconnect(self):
        """قطع الاتصال بقاعدة البيانات"""
        if self.conn:
            self.conn.close()
    
    def execute(self, query, params=None):
        """تنفيذ استعلام"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except Exception as e:
            print(f"خطأ في تنفيذ الاستعلام: {e}")
            self.conn.rollback()
            return None
    
    def fetchone(self, query, params=None):
        """جلب سجل واحد"""
        cursor = self.execute(query, params)
        return cursor.fetchone() if cursor else None
    
    def fetchall(self, query, params=None):
        """جلب جميع السجلات"""
        cursor = self.execute(query, params)
        return cursor.fetchall() if cursor else []
    
    def init_database(self):
        """تهيئة قاعدة البيانات وإنشاء الجداول"""
        if not os.path.exists(self.db_path):
            self.connect()
            self._create_tables()
            self._insert_default_data()
            print("✅ تم تهيئة قاعدة البيانات بنجاح")
        else:
            self.connect()
    
    def _create_tables(self):
        """إنشاء جداول النظام"""
        
        # جدول الحسابات والصناديق
        self.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_code TEXT UNIQUE NOT NULL,
                account_name TEXT NOT NULL,
                balance_yer REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الأصناف والمخزون
        self.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_code TEXT UNIQUE NOT NULL,
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                barcode TEXT UNIQUE,
                imei TEXT UNIQUE,
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 5,
                cost_price_yer REAL DEFAULT 0.0,
                sale_price_yer REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول العملاء
        self.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT UNIQUE,
                address TEXT,
                credit_limit REAL DEFAULT 500000.0,
                total_debt REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الموردين
        self.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT NOT NULL,
                phone TEXT UNIQUE,
                address TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول فواتير المبيعات
        self.execute('''
            CREATE TABLE IF NOT EXISTS sales_invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                invoice_date TEXT NOT NULL,
                customer_id INTEGER,
                invoice_type TEXT,
                total_amount REAL DEFAULT 0.0,
                paid_amount REAL DEFAULT 0.0,
                remaining_amount REAL DEFAULT 0.0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        ''')
        
        # جدول تفاصيل المبيعات
        self.execute('''
            CREATE TABLE IF NOT EXISTS sales_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY(invoice_id) REFERENCES sales_invoices(id),
                FOREIGN KEY(item_id) REFERENCES items(id)
            )
        ''')
        
        # جدول فواتير المشتريات
        self.execute('''
            CREATE TABLE IF NOT EXISTS purchase_invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                invoice_date TEXT NOT NULL,
                supplier_id INTEGER,
                total_amount REAL DEFAULT 0.0,
                paid_amount REAL DEFAULT 0.0,
                remaining_amount REAL DEFAULT 0.0,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
            )
        ''')
        
        # جدول تفاصيل المشتريات
        self.execute('''
            CREATE TABLE IF NOT EXISTS purchase_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY(invoice_id) REFERENCES purchase_invoices(id),
                FOREIGN KEY(item_id) REFERENCES items(id)
            )
        ''')
        
        # جدول الحركات المالية
        self.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                from_account INTEGER,
                to_account INTEGER,
                amount REAL NOT NULL,
                description TEXT,
                transaction_date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(from_account) REFERENCES accounts(id),
                FOREIGN KEY(to_account) REFERENCES accounts(id)
            )
        ''')
        
        # جدول سجل الديون
        self.execute('''
            CREATE TABLE IF NOT EXISTS customer_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                invoice_id INTEGER,
                payment_amount REAL NOT NULL,
                payment_date TEXT NOT NULL,
                payment_method TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(customer_id) REFERENCES customers(id),
                FOREIGN KEY(invoice_id) REFERENCES sales_invoices(id)
            )
        ''')
        
        print("✅ تم إنشاء جميع الجداول بنجاح")
    
    def _insert_default_data(self):
        """إدراج البيانات الافتراضية"""
        
        # إدراج الحسابات الافتراضية
        for code, name in DEFAULT_ACCOUNTS.items():
            self.execute(
                'INSERT OR IGNORE INTO accounts (account_code, account_name) VALUES (?, ?)',
                (code, name)
            )
        
        print("✅ تم إدراج البيانات الافتراضية بنجاح")

# إنشاء instance عام من قاعدة البيانات
db = Database()
