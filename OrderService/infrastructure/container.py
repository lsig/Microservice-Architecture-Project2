from dependency_injector import providers, containers
from db_connection.db_config import DbConfig
from db_connection.postgres_db_connection import PostgresDbConnection


from infrastructure.settings import Settings
from order_repository import OrderRepository
from order_service import OrderService


class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()


    db_config_provider = providers.Singleton(
        DbConfig,
        host=config.db_host,
        database=config.db_database,
        user=config.db_user,
        password=config.db_password
    )

    db_connection_provider = providers.Singleton(
        PostgresDbConnection,
        db_config=db_config_provider
    )

    order_repository_provider = providers.Singleton(
        OrderRepository,
        db_connection=db_connection_provider
    )

    order_service_provider = providers.Singleton(
        OrderService,
        order_repository=order_repository_provider
    )
