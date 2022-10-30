


from db_connection.postgres_db_connection import PostgresDbConnection
from models.order_model import OrderModel


class OrderRepository:
    def __init__(self, connection: PostgresDbConnection) -> None:
        self.__connection = connection

    def save_order(self, order: OrderModel):
        self.__connection.execute(f'''
            INSERT INTO orders(order) VALUES ('{order}')
            ''')
        self.__connection.commit()