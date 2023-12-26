import abc

from python_orders.domain.models.order import Order


class OrderSaver(abc.ABC):
    @abc.abstractmethod
    async def save_order(self, order: Order) -> None:
        raise NotImplementedError


class OrdersReader(abc.ABC):
    @abc.abstractmethod
    async def get_orders(self) -> list[Order]:
        raise NotImplementedError
