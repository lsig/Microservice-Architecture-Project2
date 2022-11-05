from models.payment_model import PaymentModel

class OrderConverter:
    def to_payment_response(self, order_object, is_valid) -> PaymentModel:
        return PaymentModel(
            orderId = order_object["id"], 
            productId = order_object["orderModel"]["productId"],
            paymentSuccess = is_valid
        )