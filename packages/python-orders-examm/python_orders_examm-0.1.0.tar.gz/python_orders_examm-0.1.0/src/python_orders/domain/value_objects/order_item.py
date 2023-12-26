from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderItem:
    name: str
    price: Decimal
    quantity: int
