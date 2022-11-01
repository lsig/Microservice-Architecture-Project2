from pydantic import BaseModel

from models.credit_card_model import CreditCardModel
from models.order_model import OrderModel



class OrderEventModel(BaseModel):
    id: int
    orderModel: OrderModel
    