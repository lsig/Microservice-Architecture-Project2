from pydantic import BaseModel

from models.credit_card_model import CreditCardModel

class OrderModel(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    creditCard: CreditCardModel
    discount: float

