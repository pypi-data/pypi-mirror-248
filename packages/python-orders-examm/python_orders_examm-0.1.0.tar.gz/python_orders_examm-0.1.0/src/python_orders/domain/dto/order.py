from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CreateItemDTO:
    name: str
    price: Decimal
    quantity: int


@dataclass(frozen=True)
class CreateOrderDTO:
    user_email: str
    items: list[CreateItemDTO]
    created_at: datetime
