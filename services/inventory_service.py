"""
خدمة إدارة المخزون
Inventory Management Service
"""

from sqlalchemy.orm import Session
from datetime import datetime
import logging

from database.models import Inventory, InventoryMovement, Product

logger = logging.getLogger(__name__)


class InventoryService:
    """خدمة إدارة المخزون"""
    
    @staticmethod
    def get_inventory(db: Session, branch_id: int, product_id: int) -> Inventory:
        """الحصول على مخزون المنتج"""
        inventory = db.query(Inventory).filter(
            Inventory.branch_id == branch_id,
            Inventory.product_id == product_id
        ).first()
        
        if not inventory:
            raise ValueError("Inventory not found")
        return inventory
    
    @staticmethod
    def update_stock(
        db: Session,
        branch_id: int,
        product_id: int,
        quantity_change: int,
        transaction_type: str,
        reference_id: int = None,
        notes: str = None
    ) -> InventoryMovement:
        """تحديث المخزون"""
        try:
            # الحصول على المخزون
            inventory = db.query(Inventory).filter(
                Inventory.branch_id == branch_id,
                Inventory.product_id == product_id
            ).first()
            
            if not inventory:
                raise ValueError("Inventory not found")
            
            # تحديث الكمية
            inventory.quantity_on_hand += quantity_change
            
            # إنشاء سجل الحركة
            movement = InventoryMovement(
                inventory_id=inventory.id,
                transaction_type=transaction_type,
                quantity_change=quantity_change,
                reference_id=reference_id,
                notes=notes,
            )
            
            db.add(movement)
            db.commit()
            
            logger.info(
                f"Inventory updated for product {product_id}: {quantity_change}"
            )
            return movement
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating inventory: {e}")
            raise
    
    @staticmethod
    def get_low_stock_items(db: Session, branch_id: int) -> list:
        """الحصول على المنتجات ذات المخزون المنخفض"""
        return db.query(Inventory).filter(
            Inventory.branch_id == branch_id,
            Inventory.quantity_on_hand <= Inventory.min_stock_level
        ).all()
    
    @staticmethod
    def transfer_stock(
        db: Session,
        from_branch_id: int,
        to_branch_id: int,
        product_id: int,
        quantity: int
    ) -> bool:
        """نقل المخزون بين الفروع"""
        try:
            # الحصول على المخزون من الفرع المصدر
            from_inventory = db.query(Inventory).filter(
                Inventory.branch_id == from_branch_id,
                Inventory.product_id == product_id
            ).first()
            
            if not from_inventory or from_inventory.quantity_on_hand < quantity:
                raise ValueError("Insufficient stock to transfer")
            
            # الحصول على المخزون من الفرع المقصد
            to_inventory = db.query(Inventory).filter(
                Inventory.branch_id == to_branch_id,
                Inventory.product_id == product_id
            ).first()
            
            if not to_inventory:
                raise ValueError("Destination inventory not found")
            
            # نقل المخزون
            from_inventory.quantity_on_hand -= quantity
            to_inventory.quantity_on_hand += quantity
            
            # تسجيل الحركات
            from_movement = InventoryMovement(
                inventory_id=from_inventory.id,
                transaction_type='transfer',
                quantity_change=-quantity,
                notes=f"Transfer to branch {to_branch_id}",
            )
            
            to_movement = InventoryMovement(
                inventory_id=to_inventory.id,
                transaction_type='transfer',
                quantity_change=quantity,
                notes=f"Transfer from branch {from_branch_id}",
            )
            
            db.add(from_movement)
            db.add(to_movement)
            db.commit()
            
            logger.info(
                f"Stock transferred: {quantity} units from branch {from_branch_id} "
                f"to branch {to_branch_id}"
            )
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error transferring stock: {e}")
            raise
    
    @staticmethod
    def get_inventory_value(db: Session, branch_id: int) -> dict:
        """حساب قيمة المخزون"""
        inventories = db.query(Inventory).filter(
            Inventory.branch_id == branch_id
        ).all()
        
        total_quantity = 0
        total_value = 0
        
        for inv in inventories:
            quantity = inv.quantity_on_hand
            product = inv.product
            
            total_quantity += quantity
            total_value += quantity * product.cost_price
        
        return {
            'total_quantity': total_quantity,
            'total_value': total_value,
            'avg_unit_value': total_value / total_quantity if total_quantity > 0 else 0,
        }
    
    @staticmethod
    def get_inventory_movement_history(
        db: Session,
        inventory_id: int,
        limit: int = 100
    ) -> list:
        """الحصول على سجل حركات المخزون"""
        return db.query(InventoryMovement).filter(
            InventoryMovement.inventory_id == inventory_id
        ).order_by(
            InventoryMovement.created_at.desc()
        ).limit(limit).all()
