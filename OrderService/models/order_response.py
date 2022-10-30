from pydantic import BaseModel


class OrderResponse(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    cardNumber: str
    totalPrice: float