# -*- coding: utf-8 -*-
"""
نموذج الصنف
"""

class Item:
    """فئة تمثل الصنف أو المنتج"""
    
    def __init__(self, item_code, item_name, category, cost_price=0.0, sale_price=0.0):
        self.item_code = item_code
        self.item_name = item_name
        self.category = category  # phones, accessories, spare_parts
        self.barcode = None
        self.imei = None  # للهواتف فقط
        self.quantity = 0
        self.cost_price = cost_price
        self.sale_price = sale_price
        self.min_quantity = 5
    
    def is_low_stock(self):
        """التحقق من انخفاض المخزون"""
        return self.quantity <= self.min_quantity
    
    def add_stock(self, quantity):
        """إضافة كمية إلى المخزون"""
        self.quantity += quantity
    
    def remove_stock(self, quantity):
        """إزالة كمية من المخزون"""
        if self.quantity >= quantity:
            self.quantity -= quantity
            return True
        return False
    
    def get_profit_margin(self):
        """حساب هامش الربح"""
        if self.cost_price == 0:
            return 0
        return ((self.sale_price - self.cost_price) / self.cost_price) * 100
