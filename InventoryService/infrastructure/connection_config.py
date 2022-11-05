from pydantic import BaseModel


class ConnectionConfig(BaseModel):
    server_ip: str
    this_port: int
    merchant_service_port: int