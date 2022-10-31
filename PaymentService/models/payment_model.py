from pydantic import BaseModel, Field


class PaymentModel(BaseModel):
    order_id: int = Field(None, alias="_id") ### better id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    product_id: int
    payment_succsess: bool


    class Config:
        schema_extra = {
            "example": {
                "order_id": 35,
                "product_id": 12,
                "payment_succsess": True
            }
        }
