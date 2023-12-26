from python_orders.domain.dto.order import CreateOrderDTO
from python_orders.domain.models.order import Order
from python_orders.domain.value_objects.order_item import OrderItem


class OrderService:
    def create_order(self, data: CreateOrderDTO) -> Order:
        return Order(
            id=None,
            created_at=data.created_at,
            user_email=data.user_email,
            items=[
                OrderItem(
                    name=item.name,
                    price=item.price,
                    quantity=item.quantity,
                )
                for item in data.items
            ],
        )
