import abc
from python_orders.application.common.use_case import UseCase
from python_orders.application.save_order.dto import SaveOrderDTO
from python_orders.application.save_order.interfaces import OrderRepository
from python_orders.domain.dto.order import CreateItemDTO, CreateOrderDTO
from python_orders.domain.services.order import OrderService


class SaveOrder(UseCase[SaveOrderDTO, None], abc.ABC):
    pass


class SaveOrderImpl(SaveOrder):
    def __init__(
        self,
        order_repository: OrderRepository,
        order_service: OrderService,
    ) -> None:
        self.order_repository = order_repository
        self.order_service = order_service

    async def __call__(self, data: SaveOrderDTO) -> None:
        order = self.order_service.create_order(
            CreateOrderDTO(
                user_email=data.user.email,
                created_at=data.created_at,
                items=[
                    CreateItemDTO(
                        name=item.name,
                        price=item.price,
                        quantity=item.quantity,
                    )
                    for item in data.items
                ],
            ),
        )
        await self.order_repository.save_order(order)
        return
