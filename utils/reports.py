# -*- coding: utf-8 -*-
"""
أداة توليد التقارير
"""

from datetime import datetime
from config import REPORTS_DIR

class ReportGenerator:
    """منشئ التقارير"""
    
    @staticmethod
    def generate_profit_loss_report(sales_data, purchases_data):
        """توليد تقرير الأرباح والخسائر"""
        total_sales = sum(item["total"] for item in sales_data)
        total_purchases = sum(item["total"] for item in purchases_data)
        net_profit = total_sales - total_purchases
        
        return {
            "total_sales": total_sales,
            "total_purchases": total_purchases,
            "net_profit": net_profit,
            "profit_margin": (net_profit / total_sales * 100) if total_sales > 0 else 0
        }
    
    @staticmethod
    def generate_inventory_report(inventory_data):
        """توليد تقرير المخزون"""
        total_items = len(inventory_data)
        total_value = sum(item["quantity"] * item["cost_price"] for item in inventory_data)
        low_stock_items = [item for item in inventory_data if item["quantity"] <= item["min_quantity"]]
        
        return {
            "total_items": total_items,
            "total_value": total_value,
            "low_stock_items": low_stock_items,
            "low_stock_count": len(low_stock_items)
        }
    
    @staticmethod
    def generate_customer_debt_report(customers_data):
        """توليد تقرير ديون العملاء"""
        total_debt = sum(customer["total_debt"] for customer in customers_data)
        customers_in_debt = [c for c in customers_data if c["total_debt"] > 0]
        
        return {
            "total_debt": total_debt,
            "customers_in_debt": customers_in_debt,
            "customers_count": len(customers_in_debt)
        }
    
    @staticmethod
    def export_to_text(report_data, filename):
        """تصدير التقرير إلى ملف نصي"""
        try:
            filepath = f"{REPORTS_DIR}/{filename}.txt"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(report_data))
            return True, filepath
        except Exception as e:
            return False, str(e)
