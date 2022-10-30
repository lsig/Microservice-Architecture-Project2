from pydantic import (BaseSettings)

class Settings(BaseSettings):
    mongodb_log_host: str
    mongodb_log_port: int
    mongodb_log_user: str
    mongodb_log_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
