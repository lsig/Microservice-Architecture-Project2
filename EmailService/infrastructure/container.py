from dependency_injector import containers, providers
from connections.email_config import EmailConfig
from connections.rabbit_config import RabbitConfig
from connections.rabbit_connection import RabbitMQConnection
from infrastructure.settings import Settings
from order_receiver import OrderEmailSender
from payment_receiver import PaymentEmailSender

class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()

    rb_config = providers.Singleton(
        RabbitConfig,
        host=config.rabbitmq_log_host,
        port=config.rabbitmq_log_port,
        user=config.rabbitmg_log_user,
        password=config.rabbitmq_log_password
    )

    email_info = providers.Singleton(
        EmailConfig,
        email=config.email,
        email_password=config.email_password
    )

    rb_connection = providers.Singleton(
        RabbitMQConnection,
        rabbit_config=rb_config
    )

    order_receiver_provider = providers.Factory(
        OrderEmailSender,
        connection=rb_connection,
        emailConfig=email_info
    )

    payment_receiver_provider = providers.Factory(
        PaymentEmailSender,
        connection=rb_connection,
        EmailConfig=email_info
    )