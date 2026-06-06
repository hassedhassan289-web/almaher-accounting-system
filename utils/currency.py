# -*- coding: utf-8 -*-
"""
أداة تحويل العملات
"""

from config import EXCHANGE_RATES, CURRENCY_SYMBOL

class CurrencyConverter:
    """محول العملات"""
    
    def __init__(self):
        self.rates = EXCHANGE_RATES.copy()
    
    def convert(self, amount, from_currency="YER", to_currency="YER"):
        """تحويل المبلغ من عملة إلى أخرى"""
        if from_currency == to_currency:
            return amount
        
        if from_currency not in self.rates or to_currency not in self.rates:
            return amount
        
        # تحويل إلى الريال اليمني أولاً ثم إلى العملة المطلوبة
        amount_in_yer = amount * self.rates[from_currency]
        converted_amount = amount_in_yer / self.rates[to_currency]
        
        return round(converted_amount, 2)
    
    def format_currency(self, amount, currency_code="YER"):
        """تنسيق المبلغ مع رمز العملة"""
        return f"{amount:,.2f} {currency_code}"
    
    def update_rate(self, currency_code, rate):
        """تحديث سعر الصرف"""
        self.rates[currency_code] = rate
    
    def get_rate(self, currency_code):
        """الحصول على سعر الصرف"""
        return self.rates.get(currency_code, 1.0)
