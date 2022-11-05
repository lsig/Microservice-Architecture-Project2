from fastapi import HTTPException
from typing import List
from requests import get

from inventory_repository import InventoryRepository
from models.product_model import ProductModel
from models.product_response_model import ProductResponseModel
from models.outside_models.payment_model import PaymentModel
from converters.inventory_converter import InventoryConverter
from infrastructure.connection_config import ConnectionConfig


class InventoryService:
    def __init__(self, inventory_repository: InventoryRepository, connection_config: ConnectionConfig) -> None:
        self.inventory_repository = inventory_repository
        self.inventory_converter = InventoryConverter()
        self.server = connection_config
        

    def get_product(self, id: int) -> ProductResponseModel:
        product: List = self.inventory_repository.get_product(id)

        if product == []:
            raise HTTPException(status_code=404, detail="Product does not exist")

        product_response: ProductResponseModel = self.inventory_converter.to_product_response(product[0])
        return product_response



    def save_products(self, product: ProductModel):
        self.validate_request(product)
        return self.inventory_repository.save_product(product)[0][0] #the sql query returns a list of products (only one product though), of which we want the first (and only) product. inside that product we want the first element (the id)



    def reserve_product(self, id: int):
        reserved: int = self.get_product_reserved_count(id)
        return self.inventory_repository.reserve_product(id, reserved)




    def process_payment(self, payment: PaymentModel):
        if payment.paymentSuccess:
            response = self.inventory_repository.remove_product(payment.productId)

        else:
            response = self.inventory_repository.remove_reservation(payment.productId)

        return response


####


    def validate_request(self, product: ProductModel):
        self.__validate_merchant(product.merchantId)
        self.__validate_price(product.price)
        self.__validate_quantity(product.quantity)

    def __validate_merchant(self, merchant_id: int):
        print(f"using {self.server.merchant_service_container}")
        merchant = get(f"http://{self.server.merchant_service_container}/merchants/{merchant_id}")

        if merchant.status_code == 404:
            raise HTTPException(status_code=400, detail=merchant.json()["detail"])

    def __validate_price(self, price: int):
        if price <= 0:
            raise HTTPException(status_code=400, detail="price must be a positive integer")
    
    def __validate_quantity(self, quantity: int):
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="quantity must be a positive integer")




    def get_product_reserved_count(self, id: int):
        product = self.get_product(id)

        if (product.quantity <= product.reserved):
            raise HTTPException(status_code=400, detail="Product is sold out")

        return product.reserved
