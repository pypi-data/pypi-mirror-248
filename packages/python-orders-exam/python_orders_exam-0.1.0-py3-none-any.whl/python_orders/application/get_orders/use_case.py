import abc
from python_orders.application.common.use_case import UseCase
from python_orders.application.get_orders.interfaces import OrderRepository
from python_orders.domain.models.order import Order


class GetOrders(UseCase[None, list[Order]], abc.ABC):
    pass


class GetOrdersImpl(GetOrders):
    def __init__(self, order_repository: OrderRepository) -> None:
        self.__order_repository = order_repository

    async def __call__(self, data: None) -> list[Order]:
        return await self.__order_repository.get_orders()
