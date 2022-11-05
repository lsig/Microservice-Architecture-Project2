from requests import get, patch
from fastapi import HTTPException


from models.order_model import OrderModel
from models.order_response import OrderResponse
from models.order_event_model import OrderEventModel
from models.outside_models.buyer_model import BuyerModel
from models.outside_models.merchant_model import MerchantModel
from models.outside_models.product_model import ProductModel

from order_repository import OrderRepository
from converters.order_converter import OrderConverter
from event_sender import EventSender
from infrastructure.connection_config import ConnectionConfig


MAX_CARD_NUMBER_LEN = 19
MIN_CARD_NUMBER_LEN = 8


class OrderService:
    def __init__(self, order_repository: OrderRepository, event_sender: EventSender, connection_config: ConnectionConfig) -> None:
        self.order_repository = order_repository
        self.event_sender = event_sender
        self.server = connection_config
        self.order_converter = OrderConverter()


    def get_order(self, id: int):
        order = self.order_repository.get_order(id)

        if order == []:
            raise HTTPException(status_code=404, detail="Order does not exist")

        order_response: OrderResponse = self.order_converter.to_order_response(order[0])
        return order_response



    def post_order(self, order: OrderModel):
        merchant: MerchantModel = self.get_merchant(order)
        buyer: BuyerModel = self.get_buyer(order)
        product: ProductModel = self.get_product(order, merchant)


        self.reserve_product(order.productId)

        order_id = self.order_repository.save_order(order, product)

        order_event: OrderEventModel = self.order_converter.to_order_event(order_id[0][0], order, merchant, buyer, product)

        self.event_sender.send_order_created_event(order_event)
        return order_id


    
    def reserve_product(self, product_id: int):
        reservation = patch(f"http://{self.server.server_ip}:{self.server.inventory_service_port}/products/reserve/{product_id}")

        if reservation.status_code != 201:
            raise HTTPException(status_code=reservation.status_code, detail=reservation.json()["detail"])



    def get_merchant(self, order: OrderModel):
        merchant_response = get(f"http://{self.server.server_ip}:{self.server.merchant_service_port}/merchants/{order.merchantId}")
        return self.__validate_merchant(merchant_response)


    def __validate_merchant(self, merchant):
        merchant_content = merchant.json()
        if merchant.status_code == 404:
            raise HTTPException(status_code=400, detail="Merchant does not exist")

        merchant_model: MerchantModel = self.order_converter.to_merchant_model(merchant_content)
        return merchant_model



    def get_buyer(self, order: OrderModel):
        buyer = get(f"http://{self.server.server_ip}:{self.server.buyer_service_port}/buyers/{order.buyerId}")
        return self.__validate_buyer(buyer)


    def __validate_buyer(self, buyer):
        buyer_content = buyer.json()
        if buyer.status_code == 404:
            raise HTTPException(status_code=400, detail="Buyer does not exist")

        buyer_model: BuyerModel = self.order_converter.to_buyer_model(buyer_content)
        return buyer_model
    


    def get_product(self, order: OrderModel, merchant: MerchantModel):
        product = get(f"http://{self.server.server_ip}:{self.server.inventory_service_port}/products/{order.productId}")
        return self.__validate_product(product, order, merchant)


    def __validate_product(self, product, order: OrderModel, merchant: MerchantModel):
        if product.status_code == 404:
            raise HTTPException(status_code=400, detail="Product does not exist")

        product_model: ProductModel = self.order_converter.to_product_model(product.json())

        if product_model.quantity <= product_model.reserved:
            raise HTTPException(status_code=400, detail="Product is sold out")
        
        if product_model.merchantId != merchant.id:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")

        if order.discount != 0:
            if not merchant.allows_discount:
                raise HTTPException(status_code=400, detail="Merchant does not allow discount")

            if order.discount < 0 or order.discount >= 1:
                raise HTTPException(status_code=400, detail="Discount must be between 0 (inclusive) and 1 (exclusive)")

            product_model.price *= (1 - order.discount)

        if not (MIN_CARD_NUMBER_LEN <= len(order.creditCard.cardNumber) <= MAX_CARD_NUMBER_LEN):
            raise HTTPException(status_code=400, detail=f"Credit card number must be between {MIN_CARD_NUMBER_LEN} and {MAX_CARD_NUMBER_LEN} (inclusive) characters")

        return product_model
        