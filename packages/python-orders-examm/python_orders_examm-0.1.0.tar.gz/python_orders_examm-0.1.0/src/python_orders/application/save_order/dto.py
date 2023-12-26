from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass

from python_orders.domain.models.email import Email
from python_orders.domain.models.order import OrderId


@dataclass(frozen=True)
class OrderUserDTO:
    email: Email


@dataclass(frozen=True)
class ItemDTO:
    name: str
    price: Decimal
    quantity: int


@dataclass(frozen=True)
class SaveOrderDTO:
    user: OrderUserDTO
    items: list[ItemDTO]
    created_at: datetime
