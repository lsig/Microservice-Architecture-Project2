import json
import requests

from connections.rabbitmq_connection import RabbitMQConnection
from emit_event import PaymentSender
from models.payment_model import PaymentModel
from models.payment_converter import OrderConverter
from payment_repository import PaymentRepository

class OrderReceiver:
    def __init__(self, connection: RabbitMQConnection, payment_repo: PaymentRepository, payment_sender: PaymentSender) -> None:
        self.order_converter = OrderConverter()
        self.payment_repo = payment_repo
        self.payment_sender = payment_sender
        self.connection = connection.connection
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="order_created", exchange_type="fanout")
        result = self.channel.queue_declare(queue='')
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange="order_created", queue=self.queue_name)

    ### Is this the best way to implement this?
    def callback(self, ch, method, properties, body):
        info = json.loads(body)
        is_valid = self.validate(info["orderModel"]["creditCard"])
        event: PaymentModel = self.order_converter.to_payment_response(info, is_valid)
        self.payment_sender.send_message(event)
        requests.post("http://localhost:8004/payments", data=event.json())
        order_id = info["id"]
        payment = requests.get(f"http://localhost:8004/payments/{order_id}")
        print(f"Payment {payment.text} succsessfully stored")
        #self.send_to_db(event)
    
    async def send_to_db(self, event):
        doc = await self.payment_repo.post_payment(event)
        payment = await self.payment_repo.fetch_payment(event["order_id"])
        print(f"Payment {payment} succsessfully stored")
        

    def consume(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()
    
    def validate(self, card_info):
        card_number = card_info["cardNumber"]
        cvc = card_info["cvc"]
        month = card_info["expirationMonth"]
        year = card_info["expirationYear"]
        is_card_valid = self.__validate_card_number(card_number)
        is_cvc_valid = self.__validate_cvc(cvc)
        is_month_valid = self.__validate_month(month)
        is_year_valid = self.__validate_year(year)
        return is_card_valid and is_cvc_valid and is_month_valid and is_year_valid
        

    def __get_digits(self, cc_number: str):
        return [int(i) for i in str(cc_number)]
    
    def __luhn_checksum(self, card_number):
        odd_digits = card_number[-1::-2]
        even_digits = card_number[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for i in even_digits:
            checksum += sum(self.__get_digits(i*2))
        return checksum % 10
    
    def __validate_card_number(self, card_number):
        card_number = self.__get_digits(card_number)
        is_valid = self.__luhn_checksum(card_number)
        return is_valid == 0
    
    def __validate_month(self, month):
        if month > 0 and month < 13:
            return True
        return False
    
    def __validate_year(self, year):
        if year > 2021 and len(str(year)) == 4:
            return True
        return False
    
    def __validate_cvc(self, cvc):
        return len(str(cvc)) == 3