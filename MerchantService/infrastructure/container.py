from dependency_injector import containers, providers
from database.db_config import DbConfig
from database.mongodb_connection import MongoDbConnection
from infrastructure.settings import Settings
from merchant_repository import MerchantRepository

class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()


    db_config = providers.Singleton(
        DbConfig,
        host=config.mongodb_log_host,
        port=config.mongodb_log_port,
        user=config.mongodb_log_user,
        password=config.mongodb_log_password
    )

    db_connection = providers.Singleton(
        MongoDbConnection,
        db_config=db_config
    )

    merchant_repository_provider = providers.Factory(
        MerchantRepository,
        connection=db_connection
    )