from pydantic import BaseModel



class ConnectionConfig(BaseModel):
    server_ip: str
    merchant_service_port: int
    buyer_service_port: int
    inventory_service_port: int
    