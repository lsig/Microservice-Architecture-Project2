from pydantic import BaseModel

class PaymentModel(BaseModel):
    id: str
    order_id: int
    product_id: int
    payment_succsess: bool