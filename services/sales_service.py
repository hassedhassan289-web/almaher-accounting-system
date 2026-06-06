"""
خدمة إدارة المبيعات
Sales Management Service
"""

from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime, date
import logging

from database.models import Sale, SaleItem, Product, Customer, Inventory, Payment
from utils.validators import validate_sale_data

logger = logging.getLogger(__name__)


class SalesService:
    """خدمة إدارة المبيعات"""
    
    @staticmethod
    def create_sale(db: Session, sale_data: dict) -> Sale:
        """إنشاء فاتورة مبيعات"""
        try:
            validate_sale_data(sale_data)
            
            # حساب المجاميع
            subtotal = Decimal(0)
            total_tax = Decimal(0)
            
            # إنشاء الفاتورة
            sale = Sale(
                invoice_number=sale_data['invoice_number'],
                branch_id=sale_data['branch_id'],
                customer_id=sale_data.get('customer_id'),
                sale_type=sale_data.get('sale_type', 'retail'),
                sale_date=sale_data.get('sale_date', date.today()),
                payment_status='pending',
                subtotal=subtotal,
                total_amount=subtotal,
            )
            
            db.add(sale)
            db.flush()
            
            # إضافة العناصر
            for item_data in sale_data.get('items', []):
                product = db.query(Product).filter(
                    Product.id == item_data['product_id']
                ).first()
                
                if not product:
                    raise ValueError(f"Product {item_data['product_id']} not found")
                
                # التحقق من المخزون
                inventory = db.query(Inventory).filter(
                    Inventory.branch_id == sale_data['branch_id'],
                    Inventory.product_id == item_data['product_id']
                ).first()
                
                if not inventory or inventory.quantity_on_hand < item_data['quantity']:
                    raise ValueError(
                        f"Insufficient stock for product {product.sku}"
                    )
                
                # إنشاء عنصر المبيعات
                unit_price = Decimal(str(item_data.get('unit_price', product.retail_price)))
                quantity = item_data['quantity']
                discount_percent = Decimal(str(item_data.get('discount_percent', 0)))
                tax_percent = Decimal(str(item_data.get('tax_percent', product.tax_rate)))
                
                # حساب المبالغ
                line_subtotal = unit_price * quantity
                discount_amount = (line_subtotal * discount_percent / 100).quantize(Decimal('0.01'))
                line_after_discount = line_subtotal - discount_amount
                tax_amount = (line_after_discount * tax_percent / 100).quantize(Decimal('0.01'))
                line_total = line_after_discount + tax_amount
                
                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=item_data['product_id'],
                    quantity=quantity,
                    unit_price=unit_price,
                    discount_percent=discount_percent,
                    discount_amount=discount_amount,
                    tax_percent=tax_percent,
                    tax_amount=tax_amount,
                    line_total=line_total,
                    serial_number=item_data.get('serial_number'),
                    notes=item_data.get('notes'),
                )
                
                db.add(sale_item)
                subtotal += line_subtotal
                total_tax += tax_amount
                
                # تحديث المخزون
                inventory.quantity_on_hand -= quantity
            
            # تحديث مجاميع الفاتورة
            discount_amount = Decimal(str(sale_data.get('discount_amount', 0)))
            sale.subtotal = subtotal
            sale.discount_amount = discount_amount
            sale.tax_amount = total_tax
            sale.total_amount = subtotal - discount_amount + total_tax
            sale.due_amount = sale.total_amount
            
            db.commit()
            db.refresh(sale)
            
            logger.info(f"Sale created: {sale.invoice_number}")
            return sale
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating sale: {e}")
            raise
    
    @staticmethod
    def get_sale(db: Session, sale_id: int) -> Sale:
        """الحصول على فاتورة مبيعات"""
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            raise ValueError(f"Sale {sale_id} not found")
        return sale
    
    @staticmethod
    def get_sales_by_date_range(
        db: Session,
        branch_id: int,
        start_date: date,
        end_date: date
    ) -> list:
        """الحصول على المبيعات حسب نطاق التاريخ"""
        return db.query(Sale).filter(
            Sale.branch_id == branch_id,
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        ).all()
    
    @staticmethod
    def get_pending_payments(db: Session, branch_id: int) -> list:
        """الحصول على المدفوعات المعلقة"""
        from utils.constants import PaymentStatus
        return db.query(Sale).filter(
            Sale.branch_id == branch_id,
            Sale.payment_status != 'paid'
        ).all()
    
    @staticmethod
    def record_payment(
        db: Session,
        sale_id: int,
        amount: Decimal,
        payment_method: str,
        reference_number: str = None
    ) -> Payment:
        """تسجيل دفع"""
        try:
            sale = db.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                raise ValueError(f"Sale {sale_id} not found")
            
            amount = Decimal(str(amount))
            
            # إنشاء سجل الدفع
            payment = Payment(
                payment_number=f"PM-{datetime.utcnow().timestamp()}",
                sale_id=sale_id,
                amount=amount,
                payment_method=payment_method,
                reference_number=reference_number,
                payment_date=date.today(),
            )
            
            db.add(payment)
            
            # تحديث حالة المبيعات
            sale.paid_amount += amount
            sale.due_amount -= amount
            
            if sale.due_amount <= 0:
                sale.payment_status = 'paid'
                sale.due_amount = Decimal(0)
            elif sale.paid_amount > 0:
                sale.payment_status = 'partial'
            
            db.commit()
            db.refresh(payment)
            
            logger.info(f"Payment recorded for sale {sale_id}: {amount}")
            return payment
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error recording payment: {e}")
            raise
    
    @staticmethod
    def calculate_daily_sales(db: Session, branch_id: int, sale_date: date) -> dict:
        """حساب مبيعات اليوم"""
        sales = db.query(Sale).filter(
            Sale.branch_id == branch_id,
            Sale.sale_date == sale_date
        ).all()
        
        total_sales = sum(Decimal(str(s.total_amount)) for s in sales)
        total_paid = sum(Decimal(str(s.paid_amount)) for s in sales)
        
        return {
            'total_sales': total_sales,
            'total_paid': total_paid,
            'count': len(sales),
        }
