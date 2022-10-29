from pydantic import (BaseSettings)

class Settings(BaseSettings):
    mongodb_log_user: str
    mongodb_log_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'