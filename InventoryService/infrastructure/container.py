from dependency_injector import providers, containers
from database.db_config import DbConfig
from database.postgres_db_connection import PostgresDbConnection

from infrastructure.settings import Settings
from inventory_repository import InventoryRepository
from inventory_service import InventoryService



class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()


    db_config_provide = providers.Singleton(
        DbConfig,
        host=config.db_host,
        database=config.db_database,
        user=config.db_user,
        password=config.db_password,
        port=config.db_port
    )

    db_connection_provide = providers.Singleton(
        PostgresDbConnection,
        db_config=db_config_provide
    )

    inventory_repository_provide = providers.Singleton(
        InventoryRepository,
        db_connection=db_connection_provide
    )

    inventory_service_provide = providers.Singleton(
        InventoryService,
        inventory_repository=inventory_repository_provide
    )
    

