"""
وحدات التحقق من الصحة
Validators Module
"""

from decimal import Decimal
import re


def validate_product_data(data: dict) -> bool:
    """التحقق من بيانات المنتج"""
    required_fields = ['name', 'sku', 'category_id', 'cost_price', 'retail_price']
    
    for field in required_fields:
        if field not in data or data[field] is None:
            raise ValueError(f"Required field {field} is missing")
    
    # التحقق من الأسعار
    try:
        cost = Decimal(str(data['cost_price']))
        retail = Decimal(str(data['retail_price']))
        
        if cost < 0 or retail < 0:
            raise ValueError("Prices cannot be negative")
        
        if retail < cost:
            raise ValueError("Retail price must be greater than cost price")
    
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid price: {e}")
    
    return True


def validate_sale_data(data: dict) -> bool:
    """التحقق من بيانات المبيعات"""
    required_fields = ['invoice_number', 'branch_id', 'items']
    
    for field in required_fields:
        if field not in data or data[field] is None:
            raise ValueError(f"Required field {field} is missing")
    
    # التحقق من العناصر
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        raise ValueError("Sale must have at least one item")
    
    for item in data['items']:
        if 'product_id' not in item or 'quantity' not in item:
            raise ValueError("Each item must have product_id and quantity")
        
        if int(item['quantity']) <= 0:
            raise ValueError("Quantity must be greater than 0")
    
    return True


def validate_email(email: str) -> bool:
    """التحقق من صحة البريد الإلكتروني"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """التحقق من صحة رقم الهاتف"""
    # تحقق من الأرقام فقط
    digits_only = re.sub(r'\D', '', phone)
    return len(digits_only) >= 10


def validate_sku(sku: str) -> bool:
    """التحقق من صحة SKU"""
    if not sku or len(sku) > 50:
        return False
    # يجب أن يحتوي على أحرف وأرقام فقط
    return re.match(r'^[a-zA-Z0-9\-_]+$', sku) is not None


def validate_positive_number(value) -> bool:
    """التحقق من أن الرقم موجب"""
    try:
        num = Decimal(str(value))
        return num > 0
    except:
        return False


def validate_non_negative_number(value) -> bool:
    """التحقق من أن الرقم غير سالب"""
    try:
        num = Decimal(str(value))
        return num >= 0
    except:
        return False


def validate_percentage(value) -> bool:
    """التحقق من صحة النسبة المئوية"""
    try:
        num = Decimal(str(value))
        return 0 <= num <= 100
    except:
        return False


def validate_username(username: str) -> bool:
    """التحقق من صحة اسم المستخدم"""
    if not username or len(username) < 3 or len(username) > 50:
        return False
    return re.match(r'^[a-zA-Z0-9_\-\.]+$', username) is not None


def validate_password(password: str) -> bool:
    """التحقق من صحة كلمة المرور"""
    if not password or len(password) < 8:
        return False
    # يجب أن تحتوي على حرف كبير وحرف صغير ورقم
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit
