from typing import List


from models.order_event_model import OrderEventModel
from models.order_response import OrderResponse
from models.order_model import OrderModel

from models.outside_models.buyer_model import BuyerModel
from models.outside_models.merchant_model import MerchantModel
from models.outside_models.product_model import ProductModel

class OrderConverter:
    def to_order_response(self, order: List[str]) -> OrderResponse:
        return OrderResponse(
            productId=order[0],
            merchantId=order[1],
            buyerId=order[2], 
            cardNumber= "*" * 12 + order[3][-4:], #TODO check whether this makes sense
            totalPrice=order[4]
        )


    def to_order_event(self, id: int, order: OrderModel, merchant: MerchantModel, buyer: BuyerModel, product: ProductModel) -> OrderEventModel:
        return OrderEventModel(
            id=id,
            orderModel=order,
            merchantModel=merchant,
            buyerModel=buyer,
            productModel=product
        )



    def to_merchant_model(self, merchant):
        return MerchantModel(
            id = merchant['_id'],
            name = merchant['name'],
            ssn = merchant['ssn'],
            email = merchant['email'],
            phone_number = merchant['phone_number'],
            allows_discount = merchant['allows_discount']
        )


    def to_buyer_model(self, buyer):
        return BuyerModel(
            id = buyer['_id'],
            name = buyer['name'],
            ssn = buyer['ssn'],
            email = buyer['email'],
            phone_number = buyer['phone_number']
        )
        
    
    def to_product_model(self, product):
        return ProductModel(
            id = product['id'],
            merchantId = product['merchantId'],
            productName = product['productName'],
            price = product['price'],
            quantity = product['quantity'],
            reserved = product['reserved']
        )