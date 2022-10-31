from models.product_response_model import ProductResponseModel


class InventoryConverter:

    def to_product_response(self, product) -> ProductResponseModel:
        return ProductResponseModel(
            merchantId = product[1],
            productName = product[2],
            price = product[3],
            quantity = product[4],
            reserved = product[5]
        )
