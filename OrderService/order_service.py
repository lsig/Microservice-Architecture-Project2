from requests import get, patch
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
        merchant = self.__validate_merchant(order)
        buyer = self.__validate_buyer(order)
        product = self.__validate_product(order, merchant)

        self.reserve_product(order.productId)

        order_id = self.order_repository.save_order(order)

        order_event: OrderEventModel = self.order_converter.to_order_event(order_id[0][0], order, merchant, buyer, product)

        self.event_sender.send_order_created_event(order_event)

        return order_id


    
    def reserve_product(self, product_id: int):
        reservation = patch(f"http://localhost:8003/products/reserve/{product_id}")

        if reservation.status_code != 201:
            raise HTTPException(status_code=reservation.status_code, detail=reservation.json()["detail"])



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
    

    def __validate_product(self, order: OrderModel, merchant):
        product = get(f"http://localhost:8003/products/{order.productId}")
        if product.status_code == 404:
            raise HTTPException(status_code=400, detail="Product does not exist")
        product_content = product.json()
        if product_content["quantity"] == 0:
            raise HTTPException(status_code=400, detail="Product is sold out")

        #TODO sækja í inventory_service allar products eftir merchantID.
        products_by_merchant = get(f"http://localhost:8003/products/all/by_merchant/{order.merchantId}") #TODO TEST THIS!!!
        product_ids_by_merchant = [product['id'] for product in products_by_merchant.json()]
        
        if order.productId not in product_ids_by_merchant:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")

        if order.discount != 0 and not merchant["allows_discount"]:
            raise HTTPException(status_code=400, detail="Merchant does not allow discount")
        return product_content
        