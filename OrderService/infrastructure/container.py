from dependency_injector import providers, containers
from db_connection.db_config import DbConfig
from db_connection.postgres_db_connection import PostgresDbConnection
from db_connection.rb_connection import RabbitMQConnection
from db_connection.rb_config import RabbitConfig
from event_sender import EventSender

from infrastructure.settings import Settings
from order_repository import OrderRepository
from order_service import OrderService
from infrastructure.connection_config import ConnectionConfig


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
        connection=db_connection_provider
    )

    rb_config= providers.Singleton(
        RabbitConfig,
        host=config.rabbitmq_log_host,
        port=config.rabbitmq_log_port,
        user=config.q_user,
        password=config.q_password
    )

    rb_connection = providers.Singleton(
        RabbitMQConnection,
        rabbit_config=rb_config
    )

    event_sender_provider = providers.Factory( #TODO check whether factory or singleton
        EventSender,
        connection=rb_connection
    )


    connection_config_provide = providers.Singleton(
        ConnectionConfig,
        app_host=config.app_host
    )

    order_service_provider = providers.Singleton(
        OrderService,
        order_repository=order_repository_provider,
        event_sender=event_sender_provider,
        connection_config=connection_config_provide
    )
