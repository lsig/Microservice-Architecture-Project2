from fastapi import HTTPException
from inventory_repository import InventoryRepository
from models.product_model import ProductModel
from models.product_response_model import ProductResponseModel
from converters.inventory_converter import InventoryConverter


class InventoryService:
    def __init__(self, inventory_repository: InventoryRepository) -> None:
        self.inventory_repository = inventory_repository
        self.inventory_converter = InventoryConverter()
        

    def get_product(self, id: int):
        product = self.inventory_repository.get_product(id)

        if product == []:
            raise HTTPException(status_code=404, detail="Product does not exist")

        product_response: ProductResponseModel = self.inventory_converter.to_product_response(product[0])

        return product_response

    def save_products(self, product: ProductModel):
        return self.inventory_repository.save_product(product)