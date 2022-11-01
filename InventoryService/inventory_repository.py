


from database.db_connection import DbConnection
from models.product_model import ProductModel
from models.product_response_model import ProductResponseModel


class InventoryRepository:
    def __init__(self, db_connection: DbConnection) -> None:
        self.__connection = db_connection


    def get_product(self, id: int) -> ProductResponseModel:
        product = self.__connection.execute(f'''
        SELECT * FROM products WHERE id = {id} LIMIT 1
        ''')

        return product


    def save_product(self, product: ProductModel):
        id = self.__connection.execute(f'''
        INSERT INTO products(merchantid, productname, price, quantity, reserved) 
        VALUES ('{product.merchantId}', '{product.productName}', '{product.price}', '{product.quantity}', '0')
        RETURNING id;
        ''')

        self.__connection.commit()
        return id


    def reserve_product(self, id: int, reserved: int):
        self.__connection.execute(f'''
        UPDATE products SET reserved = {reserved + 1} WHERE id = {id}
        ''')

        self.__connection.commit()
