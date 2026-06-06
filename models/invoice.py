# -*- coding: utf-8 -*-
"""
نموذج الفاتورة
"""

from datetime import datetime

class Invoice:
    """فئة تمثل الفاتورة"""
    
    def __init__(self, invoice_number, customer_id=None, invoice_type="cash"):
        self.invoice_number = invoice_number
        self.invoice_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.customer_id = customer_id
        self.invoice_type = invoice_type  # cash أو credit
        self.items = []
        self.total_amount = 0.0
        self.paid_amount = 0.0
        self.remaining_amount = 0.0
        self.notes = ""
    
    def add_item(self, item_id, quantity, unit_price):
        """إضافة صنف إلى الفاتورة"""
        item_total = quantity * unit_price
        self.items.append({
            "item_id": item_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": item_total
        })
        self.calculate_total()
    
    def calculate_total(self):
        """حساب إجمالي الفاتورة"""
        self.total_amount = sum(item["total_price"] for item in self.items)
        self.remaining_amount = self.total_amount - self.paid_amount
    
    def add_payment(self, amount):
        """إضافة دفعة للفاتورة"""
        self.paid_amount += amount
        self.calculate_total()
