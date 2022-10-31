


from db_connection.postgres_db_connection import PostgresDbConnection
from models.order_model import OrderModel


class OrderRepository:
    def __init__(self, connection: PostgresDbConnection) -> None:
        self.__connection = connection


    def get_order(self, id: int):
        order = self.__connection.execute(f'''
        SELECT * FROM orders WHERE id = {id} LIMIT 1
        ''')

        return order
    

    def save_order(self, order: OrderModel):

        id = self.__connection.execute(f'''
            INSERT INTO orders(productid, buyerid, cardnumber, totalprice) 
            VALUES ('{order.productId}', '{order.buyerId}', '{order.creditCard.cardNumber}', '100')
            RETURNING id;
            ''')

        self.__connection.commit()

        return id