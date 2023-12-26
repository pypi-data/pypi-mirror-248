from python_orders.application.common.interfaces.orders import OrdersReader
import abc


class OrderRepository(OrdersReader, abc.ABC):
    pass
