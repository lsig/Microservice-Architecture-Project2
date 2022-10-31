


from typing import List

from models.order_response import OrderResponse

class OrderConverter:
    def to_order_response(self, order: List[str]):
        return OrderResponse(
            productId=order[0],
            merchantId=order[1],
            buyerId=order[2],
            cardNumber= "*" * 12 + order[3][-4:],
            totalPrice=order[4]
        )
        