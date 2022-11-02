from pydantic import BaseModel

from models.credit_card_model import CreditCardModel
from models.order_model import OrderModel

from models.outside_models.merchant_model import MerchantModel
from models.outside_models.buyer_model import BuyerModel
from models.outside_models.product_model import ProductModel



class OrderEventModel(BaseModel):
    id: int
    orderModel: OrderModel
    merchantModel: MerchantModel
    buyerModel: BuyerModel
    productModel: ProductModel
