from pydantic import BaseModel

class MerchantModel(BaseModel):
    name: str
    ssn: str
    email: str
    phone_number: str
    allows_discount: bool