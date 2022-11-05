from pydantic import BaseModel



class ConnectionConfig(BaseModel):
    merchant_service_container: str
    buyer_service_container: str
    inventory_service_container: str
    