from pydantic import BaseModel

class PaymentModel(BaseModel):
    id: str
    orderId: int
    productId: int
    paymentSuccess: bool