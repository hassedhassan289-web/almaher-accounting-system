# -*- coding: utf-8 -*-
"""
نموذج العميل
"""

class Customer:
    """فئة تمثل العميل"""
    
    def __init__(self, customer_name, phone=None, address=None):
        self.customer_name = customer_name
        self.phone = phone
        self.address = address
        self.credit_limit = 500000.0  # الحد الأقصى للائتمان بالريال
        self.total_debt = 0.0
        self.transactions = []  # سجل المعاملات
    
    def add_debt(self, amount):
        """إضافة دين للعميل"""
        if self.total_debt + amount <= self.credit_limit:
            self.total_debt += amount
            return True
        return False  # تجاوز الحد الأقصى
    
    def pay_debt(self, amount):
        """سداد جزء من الدين"""
        if amount <= self.total_debt:
            self.total_debt -= amount
            return True
        return False
    
    def get_remaining_credit(self):
        """الحصول على الرصيد المتبقي"""
        return self.credit_limit - self.total_debt
