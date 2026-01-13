"""
Centralized constants for shop app.

This file contains all fixed values used in the project.
Change them in ONE PLACE only.
"""

# =========================================================
# ORDER STATUSES
# =========================================================

# Constant 1: Order pending (not yet confirmed)
ORDER_STATUS_PENDING = 'pending'

# Constant 2: Order confirmed (payment received)
ORDER_STATUS_CONFIRMED = 'confirmed'

# Constant 3: Order shipped (in transit)
ORDER_STATUS_SHIPPED = 'shipped'

# Constant 4: Order delivered (arrived to customer)
ORDER_STATUS_DELIVERED = 'delivered'

# Constant 5: Order cancelled (customer cancelled)
ORDER_STATUS_CANCELLED = 'cancelled'

# Tuple list for Django ChoiceField (display to user)
ORDER_STATUS_CHOICES = [
    (ORDER_STATUS_PENDING, 'Pending'),
    (ORDER_STATUS_CONFIRMED, 'Confirmed'),
    (ORDER_STATUS_SHIPPED, 'Shipped'),
    (ORDER_STATUS_DELIVERED, 'Delivered'),
    (ORDER_STATUS_CANCELLED, 'Cancelled'),
]

# =========================================================
# CATEGORY VALIDATION
# =========================================================
MAX_CATEGORY_NAME_LENGTH = 100

# =========================================================
# PRICE VALIDATION
# =========================================================

# Minimum price (cannot sell at 0€)
MIN_PRICE = 0.01

# Maximum price (limit 999,999.99€)
MAX_PRICE = 999999.99

# =========================================================
# QUANTITY VALIDATION
# =========================================================

# Minimum quantity (cannot order 0 products)
MIN_QUANTITY = 1

# Maximum quantity (cannot order 1000+ products)
MAX_QUANTITY = 1000

# =========================================================
# STOCK VALIDATION
# =========================================================

# Minimum stock to consider product "out of stock"
MIN_STOCK = 0

# Maximum stock (database limit)
MAX_STOCK = 100000

# =========================================================
# PRODUCT IMAGE UPLOAD PATH
# =========================================================
PRODUCT_IMAGE_UPLOAD_PATH = 'products/%Y/%m/'

# =========================================================
# CUSTOMER VALIDATION
# =========================================================
MAX_CUSTOMER_NAME_LENGTH = 100
MAX_CUSTOMER_EMAIL_LENGTH = 255
