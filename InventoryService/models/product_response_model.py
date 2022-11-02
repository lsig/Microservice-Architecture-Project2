from pydantic import BaseModel


class ProductResponseModel(BaseModel):
    id: int
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int