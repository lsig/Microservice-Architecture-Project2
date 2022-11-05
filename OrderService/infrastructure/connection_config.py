from pydantic import BaseModel



class ConnectionConfig(BaseModel):
    server_ip: str