from pydantic import (BaseSettings)

class Settings(BaseSettings):
    rabbitmq_log_host: str
    rabbitmq_log_port: str
    rabbitmg_log_user: str
    rabbitmq_log_password: str

    email: str
    email_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'