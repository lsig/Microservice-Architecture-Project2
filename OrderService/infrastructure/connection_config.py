from pydantic import BaseModel



class ConnectionConfig(BaseModel):
    app_host: str