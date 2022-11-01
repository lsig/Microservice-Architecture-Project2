from models.payment_model import PaymentModel

class OrderConverter:
    def to_payment_response(self, order_object, is_valid) -> PaymentModel:
        return PaymentModel(
            order_id = order_object["id"], 
            product_id = order_object["orderModel"]["productId"],
            payment_succsess = is_valid
        )