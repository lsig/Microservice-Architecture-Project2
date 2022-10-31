from pydantic import BaseModel


class ProductResponseModel(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int