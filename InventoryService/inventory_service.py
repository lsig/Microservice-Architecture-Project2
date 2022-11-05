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
        self.validate_merchant(product.merchantId)
        return self.inventory_repository.save_product(product)


    def reserve_product(self, id: int):
        reserved: int = self.get_product_reserved_count(id)

        return self.inventory_repository.reserve_product(id, reserved)



    def process_payment(self, payment: PaymentModel):
        if payment.payment_succsess:
            response = self.inventory_repository.remove_product(payment.product_id)

        else:
            response = self.inventory_repository.remove_reservation(payment.product_id)

        return response


####


    def validate_merchant(self, merchant_id: int):
        merchant = get(f"http://{self.server.server_ip}:{self.server.merchant_service_port}/merchants/{merchant_id}")

        if merchant.status_code == 404:
            raise HTTPException(status_code=400, detail=merchant.json()["detail"])




    def get_product_reserved_count(self, id: int):
        product = self.get_product(id)

        if (product.quantity <= product.reserved):
            raise HTTPException(status_code=400, detail="Product is sold out")

        return product.reserved


