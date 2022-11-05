from pydantic import BaseModel


class MerchantResponse(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool