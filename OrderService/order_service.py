from requests import get
from fastapi import HTTPException


from models.order_model import OrderModel
from models.order_response import OrderResponse
from models.order_event_model import OrderEventModel
from order_repository import OrderRepository
from converters.order_converter import OrderConverter
from event_sender import EventSender


class OrderService:
    def __init__(self, order_repository: OrderRepository, event_sender: EventSender) -> None:
        self.order_repository = order_repository
        self.event_sender = event_sender
        self.order_converter = OrderConverter()


    def get_order(self, id: int):

        order = self.order_repository.get_order(id)

        if order == []:
            raise HTTPException(status_code=404, detail="Order does not exist")

        order_response: OrderResponse = self.order_converter.to_order_response(order[0])

        return order_response



    def post_order(self, order: OrderModel):
        #self.reserve_product(order.productId)
        merchant = self.__validate_merchant(order)
        buyer = self.__validate_buyer(order)
        product = self.__validate_product(order)
        order_id = self.order_repository.save_order(order)

        order_event: OrderEventModel = self.order_converter.to_order_event(order_id[0][0], order)

        self.event_sender.send_order_created_event(order_event)

        return order_id


    def __validate_merchant(self, order: OrderModel):
        merchant = get(f"http://localhost:8001/merchants/{order.merchantId}")
        merchant_content = merchant.json()
        if merchant.status_code == 404:
            raise HTTPException(status_code=400, detail="Merchant does not exist")
        return merchant_content

    def __validate_buyer(self, order: OrderModel):
        buyer = get(f"http://localhost:8002/buyers/{order.buyerId}")
        buyer_content = buyer.json()
        if buyer.status_code == 404:
            raise HTTPException(status_code=400, detail="Buyer does not exist")
        return buyer_content
    
    def __validate_product(self, order: OrderModel):
        product = get(f"http://localhost:8003/products/{order.productId}")
        if product.status_code == 404:
            raise HTTPException(status_code=400, detail="Product does not exist")
        product_content = product.json()
        if product_content["amount"] == 0:
            raise HTTPException(status_code=400, detail="Product is sold out")

        if order.productId not in merchant_content["products"]:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")

        if order.discount != 0 and not merchant_content["allows discount"]:
            raise HTTPException(status_code=400, detail="Merchant does not allow discount")
        return product_content
        




   