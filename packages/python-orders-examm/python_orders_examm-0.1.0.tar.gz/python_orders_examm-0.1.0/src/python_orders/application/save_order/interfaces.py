from python_orders.application.common.interfaces.orders import OrderSaver, OrdersReader
import abc


class OrderRepository(OrderSaver, OrdersReader, abc.ABC):
    pass
