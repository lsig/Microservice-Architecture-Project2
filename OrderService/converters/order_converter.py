


from typing import List
from models.order_event_model import OrderEventModel
from models.order_model import OrderModel

from models.order_response import OrderResponse

class OrderConverter:
    def to_order_response(self, order: List[str]) -> OrderResponse:
        return OrderResponse(
            productId=order[0],
            merchantId=order[1],
            buyerId=order[2], 
            cardNumber= "*" * 12 + order[3][-4:], #TODO check whether this makes sense
            totalPrice=order[4]
        )


    def to_order_event(self, id: int, order: OrderModel) -> OrderEventModel:
        return OrderEventModel(
            id=id,
            orderModel=order
        )
        