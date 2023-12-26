from python_orders.adapters.db.json.orders.repository import JSONOrdersRepository
from di import Container, bind_by_type
from di.dependent import Dependent
from python_orders.application.get_orders.interfaces import (
    OrderRepository as GetOrdersOrderRepository,
)
from python_orders.application.get_orders.use_case import GetOrders, GetOrdersImpl
from python_orders.application.save_order.interfaces import (
    OrderRepository as SaveOrderOrderRepository,
)
from python_orders.application.save_order.use_case import SaveOrder, SaveOrderImpl


async def build_di() -> Container:
    container = Container()
    container.bind(bind_by_type(Dependent(SaveOrderImpl, scope="request"), SaveOrder))
    container.bind(bind_by_type(Dependent(GetOrdersImpl, scope="request"), GetOrders))
    container.bind(
        bind_by_type(
            Dependent(JSONOrdersRepository, scope="request"),
            SaveOrderOrderRepository,
            covariant=True,
        ),
    )
    container.bind(
        bind_by_type(
            Dependent(JSONOrdersRepository, scope="request"),
            GetOrdersOrderRepository,
            covariant=True,
        ),
    )
    return container
