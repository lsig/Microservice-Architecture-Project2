import yagmail
import json
from connections.email_config import EmailConfig
from connections.rabbit_connection import RabbitMQConnection

class PaymentEmailSender:
    def __init__(self, connection: RabbitMQConnection, emailConfig: EmailConfig) -> None:
        # TODO: initate connection
        self.connection = connection.connection
        self.email = yagmail.SMTP(emailConfig.email, emailConfig.email_password)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="payment", exchange_type="fanout")
        result = self.channel.queue_declare(queue='')
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange="payment", queue=self.queue_name)

    def callback(self, ch, method, properties, body):
        order = json.loads(body)
        order_id = order["order_id"]
        success = order["payment_succsess"]
        if success:
            contents = [
                f"Order {order_id} has been successfully purchased"
            ]
        else: 
            contents = [
                f"Order {order_id} purchase has failed"
            ]

        self.email.send("myuser@gmail.com", "Order has been created", contents)
        

    def consume(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()