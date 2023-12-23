from enum import Enum


class Duration(Enum):
    once = "once"
    forever = "forever"
    repeating = "repeating"


class EventType(Enum):
    order_created = "order.created"
    order_updated = "order.updated"
    order_deleted = "order.deleted"


class Interval(Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class ItemType(Enum):
    value = "value"
    percentage = "percentage"


class OrderType(Enum):
    UPGRADE = "UPGRADE"
    SHOP = "SHOP"


class PaymentProcessor(Enum):
    PAYPAL = "PAYPAL"
    STRIPE = "STRIPE"


class ProductType(Enum):
    DISCORD_ROLE = "DISCORD_ROLE"
    SHOP_PRODUCT = "SHOP_PRODUCT"
