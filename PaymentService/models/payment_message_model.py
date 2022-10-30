from pydantic import BaseModel

class PaymentMessageModel(BaseModel):
    order_id: str
    payment_succsess: bool