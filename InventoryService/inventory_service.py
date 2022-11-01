from fastapi import HTTPException, BackgroundTasks
from inventory_repository import InventoryRepository
from models.product_model import ProductModel
from models.product_response_model import ProductResponseModel
from converters.inventory_converter import InventoryConverter


class InventoryService:
    def __init__(self, inventory_repository: InventoryRepository) -> None:
        self.inventory_repository = inventory_repository
        self.inventory_converter = InventoryConverter()
        

    def get_product(self, id: int) -> ProductResponseModel:
        product = self.inventory_repository.get_product(id)

        if product == []:
            raise HTTPException(status_code=404, detail="Product does not exist")

        product_response: ProductResponseModel = self.inventory_converter.to_product_response(product[0])

        return product_response



    def save_products(self, product: ProductModel):
        return self.inventory_repository.save_product(product)



    def reserve_product(self, id: int):
        reserved: int = self.get_product_reserved_count(id)

        return self.inventory_repository.reserve_product(id, reserved)


    def get_product_reserved_count(self, id: int):
        product = self.get_product(id)

        if (product.quantity <= product.reserved):
            raise HTTPException(status_code=400, detail="Product is sold out")

        return product.reserved


