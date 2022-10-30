
from models.order_model import OrderModel
from order_repository import OrderRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    def post_order(self, order: OrderModel):
        self.validate(order)

        return "made it to order_service"


        
        #self.order_repository.save_order(order)

    
    def validate(self, order: OrderModel):
        pass