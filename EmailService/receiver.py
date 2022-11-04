import yagmail
import json
from connections.email_config import EmailConfig
from connections.rabbit_connection import RabbitMQConnection

class Sender:
    def __init__(self, connection: RabbitMQConnection, emailConfig: EmailConfig) -> None:
        self.connection = connection.connection
        self.email = yagmail.SMTP(emailConfig.email, emailConfig.email_password)
        self.channel = self.connection.channel()
        self.declare_order_exchange()
        self.declare_payment_exchange()
    
    def callback1(self, ch, method, properties, body):
        print("Order received")
        order = json.loads(body)
        order_model = order["orderModel"]
        order_id = order["id"]
        order_name = order_model["productId"] #TODO we need productName (get this in orderService/service - validate())
        order_price = 100#order_model["totalPrice"]
        contents = [
            f"Order ID: {order_id}\nProduct name: {order_name}\nPrice: {order_price}"
        ]
        self.email.send("project2.honnun@gmail.com", "Ég veit leyndarmálið þitt Baldvin...", contents)

    
    def callback2(self, ch, method, properties, body):
        print("Payment event received")
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

        self.email.send("project2.honnun@gmail.com", "Order has been created", contents)

    def declare_order_exchange(self):
        self.channel.exchange_declare(exchange="order_created", exchange_type="fanout")
        self.channel.queue_declare(queue="order_queue")
        self.queue_name1 = "order_queue"
        self.channel.queue_bind(exchange="order_created", queue=self.queue_name1)
    
    def declare_payment_exchange(self):
        self.channel.exchange_declare(exchange="payment", exchange_type="fanout")
        self.channel.queue_declare(queue="payment_queue")
        self.queue_name2 = "payment_queue"
        self.channel.queue_bind(exchange="payment", queue=self.queue_name2)
    
    def consume_order(self):
        self.channel.basic_consume(queue=self.queue_name1, on_message_callback=self.callback1, auto_ack=True)
    
    def consume_payment(self):
        self.channel.basic_consume(queue=self.queue_name2, on_message_callback=self.callback2, auto_ack=True)
    
    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.consume_order()
        self.consume_payment()
        self.channel.start_consuming()
        