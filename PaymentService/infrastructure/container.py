from dependency_injector import containers, providers
from connections.db_config import DbConfig
from connections.mongodb_connection import MongoDbConnection
from connections.rabbit_config import RabbitConfig
from connections.rabbitmq_connection import RabbitMQConnection
from emit_event import PaymentSender
from infrastructure.settings import Settings
from payment_repository import PaymentRepository
from receive_event import OrderReceiver

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

    rb_config = providers.Singleton(
        RabbitConfig,
        host=config.rabbitmq_log_host,
        port=config.rabbitmq_log_port,
        user=config.rabbitmg_log_user,
        password=config.rabbitmq_log_password
    )

    rb_connection = providers.Singleton(
        RabbitMQConnection,
        rabbit_config=rb_config
    )

    payment_repository_provider = providers.Factory(
        PaymentRepository,
        connection=db_connection
    )

    order_receiver_provider = providers.Factory(
        OrderReceiver,
        connection=rb_connection
    )

    payment_sender_provider = providers.Factory(
        PaymentSender,
        connection=rb_connection
    )