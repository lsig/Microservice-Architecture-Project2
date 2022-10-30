from fastapi import Depends
from dependency_injector.wiring import Provide
from infrastructure.container import Container


from models.order_model import OrderModel
from order_repository import OrderRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository = Depends(Provide[Container.order_repository_provider])) -> None:
        self.order_repository = order_repository

    def post_orders(self, order: OrderModel):
        self.validate(order)

        self.order_repository.save_order(order)

    
    def validate(self, order: OrderModel):
        pass