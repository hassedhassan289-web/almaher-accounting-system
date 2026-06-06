"""
خدمة إدارة المنتجات
Product Management Service
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from decimal import Decimal
from datetime import datetime
import logging

from database.models import Product, Category, Brand, Inventory
from utils.validators import validate_product_data

logger = logging.getLogger(__name__)


class ProductService:
    """خدمة إدارة المنتجات"""
    
    @staticmethod
    def create_product(db: Session, product_data: dict) -> Product:
        """إنشاء منتج جديد"""
        try:
            # التحقق من البيانات
            validate_product_data(product_data)
            
            # التحقق من تفرد SKU
            existing = db.query(Product).filter(
                Product.sku == product_data['sku']
            ).first()
            if existing:
                raise ValueError(f"SKU {product_data['sku']} موجود بالفعل")
            
            # إنشاء المنتج
            product = Product(
                name=product_data['name'],
                sku=product_data['sku'],
                barcode=product_data.get('barcode'),
                description=product_data.get('description'),
                category_id=product_data['category_id'],
                brand_id=product_data.get('brand_id'),
                cost_price=Decimal(str(product_data['cost_price'])),
                retail_price=Decimal(str(product_data['retail_price'])),
                wholesale_price=Decimal(str(product_data.get('wholesale_price', 0))),
                distributor_price=Decimal(str(product_data.get('distributor_price', 0))),
                unit=product_data.get('unit', 'piece'),
                weight=product_data.get('weight'),
                color=product_data.get('color'),
                model=product_data.get('model'),
                warranty_months=product_data.get('warranty_months', 12),
                is_active=product_data.get('is_active', True),
                is_serialized=product_data.get('is_serialized', False),
                is_perishable=product_data.get('is_perishable', False),
                tax_rate=Decimal(str(product_data.get('tax_rate', 0))),
                image_url=product_data.get('image_url'),
            )
            
            db.add(product)
            db.commit()
            db.refresh(product)
            
            logger.info(f"Product created: {product.sku} - {product.name}")
            return product
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating product: {e}")
            raise
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_data: dict) -> Product:
        """تحديث منتج"""
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            # تحديث البيانات
            for key, value in product_data.items():
                if key in ['cost_price', 'retail_price', 'wholesale_price', 'tax_rate']:
                    value = Decimal(str(value))
                if hasattr(product, key):
                    setattr(product, key, value)
            
            product.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(product)
            
            logger.info(f"Product updated: {product.sku}")
            return product
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating product: {e}")
            raise
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        """الحصول على منتج"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")
        return product
    
    @staticmethod
    def get_product_by_sku(db: Session, sku: str) -> Product:
        """الحصول على منتج بـ SKU"""
        product = db.query(Product).filter(Product.sku == sku).first()
        if not product:
            raise ValueError(f"Product with SKU {sku} not found")
        return product
    
    @staticmethod
    def search_products(db: Session, query: str, category_id: int = None) -> list:
        """البحث عن المنتجات"""
        try:
            q = db.query(Product).filter(
                Product.is_active == True,
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.sku.ilike(f"%{query}%"),
                    Product.barcode.ilike(f"%{query}%")
                )
            )
            
            if category_id:
                q = q.filter(Product.category_id == category_id)
            
            return q.all()
            
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            raise
    
    @staticmethod
    def get_products_by_category(db: Session, category_id: int) -> list:
        """الحصول على المنتجات حسب التصنيف"""
        return db.query(Product).filter(
            Product.category_id == category_id,
            Product.is_active == True
        ).all()
    
    @staticmethod
    def get_low_stock_products(db: Session, branch_id: int) -> list:
        """الحصول على المنتجات ذات المخزون المنخفض"""
        return db.query(Product).join(Inventory).filter(
            Inventory.branch_id == branch_id,
            Inventory.quantity_on_hand <= Inventory.min_stock_level,
            Product.is_active == True
        ).all()
    
    @staticmethod
    def deactivate_product(db: Session, product_id: int) -> Product:
        """تعطيل منتج"""
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            product.is_active = False
            product.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(product)
            
            logger.info(f"Product deactivated: {product.sku}")
            return product
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deactivating product: {e}")
            raise
    
    @staticmethod
    def calculate_profit_margin(cost_price: Decimal, selling_price: Decimal) -> Decimal:
        """حساب هامش الربح"""
        if cost_price == 0:
            return Decimal(0)
        return ((selling_price - cost_price) / cost_price * 100).quantize(Decimal('0.01'))
    
    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> list:
        """الحصول على جميع المنتجات"""
        return db.query(Product).filter(
            Product.is_active == True
        ).offset(skip).limit(limit).all()
