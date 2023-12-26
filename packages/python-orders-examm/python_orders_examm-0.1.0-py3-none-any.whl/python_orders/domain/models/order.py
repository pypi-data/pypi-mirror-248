from dataclasses import dataclass
from typing import NewType
from datetime import datetime
from python_orders.domain.value_objects.order_item import OrderItem

OrderId = NewType("OrderId", int)


@dataclass
class Order:
    id: OrderId | None
    user_email: str
    items: list[OrderItem]
    created_at: datetime
