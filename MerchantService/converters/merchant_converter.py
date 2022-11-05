
from models.merchant_response import MerchantResponse

class MerchantConverter:


    def to_merchant_response(self, merchant):
        return MerchantResponse(
            name=merchant['name'],
            ssn=merchant['ssn'],
            email=merchant['email'],
            phoneNumber=merchant['phone_number'],
            allowsDiscount=merchant['allows_discount']
        )