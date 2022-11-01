import yagmail
import json
from connections.email_config import EmailConfig
from connections.rabbit_connection import RabbitMQConnection


class OrderEmailSender:
    def __init__(self, connection: RabbitMQConnection, emailConfig: EmailConfig) -> None:
        # TODO: initate connection
        self.connection = connection.connection
        self.email = yagmail.SMTP(emailConfig.email, emailConfig.email_password)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="order_created", exchange_type="fanout")
        result = self.channel.queue_declare(queue='')
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange="order_created", queue=self.queue_name)

    def callback(self, ch, method, properties, body):
        order = json.loads(body)
        order_id = order["orderId"]
        order_name = order["productName"]
        order_price = order["totalPrice"]
        contents = [
            f"Order ID: {order_id}\nProduct name: {order_name}\nPrice: {order_price}"
        ]
        self.email.send("myuser@gmail.com", "Order has been created", contents)

        
    def consume(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()