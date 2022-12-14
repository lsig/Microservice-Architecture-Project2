from pydantic import BaseModel


class MerchantModel(BaseModel):
    id: int
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool