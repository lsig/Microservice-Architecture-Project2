from models.buyer_response import BuyerResponse


class BuyerConverter:

    def to_buyer_response(self, buyer) -> BuyerResponse:
        return BuyerResponse(
            name=buyer['name'],
            ssn=buyer['ssn'],
            email=buyer['email'],
            phoneNumber=buyer['phone_number']
        )
