from typing import List

from models.product_response_model import ProductResponseModel


class InventoryConverter:

    def to_product_response(self, product) -> ProductResponseModel:
        return ProductResponseModel(
            id = product[0],
            merchantId = product[1],
            productName = product[2],
            price = product[3],
            quantity = product[4],
            reserved = product[5]
        )


    def to_product_list_response(self, products) -> List[ProductResponseModel]:
        product_list_response = []
        for product in products:
            product_list_response.append(product)

        return product_list_response