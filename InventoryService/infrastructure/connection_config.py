from pydantic import BaseModel


class ConnectionConfig(BaseModel):
    merchant_service_container: str