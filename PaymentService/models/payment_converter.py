from payment_model import PaymentModel

class OrderConverter:
    def to_payment_response(self, order_object, is_valid) -> PaymentModel:
        return PaymentModel(
            order_id = order_object["orderId"], 
            product_id = order_object["productId"],
            payment_succsess = is_valid
        )