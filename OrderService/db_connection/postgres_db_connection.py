import os
import psycopg2

from db_connection.db_config import DbConfig
from db_connection.db_connection import DbConnection

class PostgresDbConnection(DbConnection):
    def __init__(self, db_config: DbConfig) -> None:
        self.__connection = psycopg2.connect(**db_config.dict())
        self.run_migrations()

    def execute(self, sql):
        cursor = self.__connection.cursor()
        cursor.execute(sql)

        #TODO check whether this is necessary. used in lab 10
        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            return []


    def commit(self) -> None:
        self.__connection.commit()
    

    def run_migrations(self):
        dir = './db_connection/migration_scripts'
        for filename in os.listdir(dir):
            with open(f'{dir}/{filename}') as fileobj:
                self.execute(fileobj.read())

        self.commit()

