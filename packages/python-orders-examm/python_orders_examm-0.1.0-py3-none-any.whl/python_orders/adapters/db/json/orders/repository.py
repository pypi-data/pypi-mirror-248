import asyncio
from python_orders.adapters.db.json.config import JSONConfig
from python_orders.application.common.interfaces.orders import OrderSaver, OrdersReader
import dataclass_factory
import aiofiles
import json
from python_orders.domain.models.order import Order, OrderId


class JSONOrdersRepository(OrderSaver, OrdersReader):
    def __init__(
        self,
        factory: dataclass_factory.Factory,
        config: JSONConfig,
    ) -> None:
        self.__factory = factory
        self.__config = config
        self.__lock = asyncio.Lock()

    async def save_order(self, order: Order) -> None:
        async with self.__lock:
            orders = await self.get_orders()

            if len(orders) > 0:
                order.id = order.id or OrderId(orders[-1].id + 1)
            else:
                order.id = order.id or 1

            replaced = False
            for i, existing_order in enumerate(orders):
                if order.id == existing_order.id:
                    orders[i] = order
                    replaced = True

            if not replaced:
                orders.append(order)

            sorted(orders, key=lambda order: order.id, reverse=True)

            orders_dict = self.__factory.dump(
                orders,
                list[Order],
            )

            async with aiofiles.open(
                self.__config.orders_json_file_path, mode="w"
            ) as f:
                await f.write(json.dumps(orders_dict))

    async def get_orders(self) -> list[Order]:
        async with aiofiles.open(self.__config.orders_json_file_path, mode="r") as f:
            file_data = await f.read()

        if len(file_data) == 0:
            return []

        try:
            orders_dict = json.loads(file_data)
        except json.JSONDecodeError:
            return []

        return self.__factory.load(
            orders_dict,
            list[Order],
        )
