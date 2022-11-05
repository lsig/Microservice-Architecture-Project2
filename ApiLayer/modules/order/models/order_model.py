from pydantic import BaseModel
from typing import Union

from modules.order.models.credit_card_model import CreditCardModel


class OrderModel(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    creditCard: CreditCardModel
    discount: Union[float, None]