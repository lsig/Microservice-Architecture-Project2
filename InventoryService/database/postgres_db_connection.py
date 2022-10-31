import psycopg2
import os

from database.db_config import DbConfig
from database.db_connection import DbConnection


class PostgresDbConnection(DbConnection):
    def __init__(self, db_config: DbConfig) -> None:
        self.__connection = psycopg2.connect(**db_config.dict())
        self.run_migrations()
        super().__init__()


    def execute(self, sql):
        cursor = self.__connection.cursor()
        cursor.execute(sql)

        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            return []


    def commit(self):
        self.__connection.commit()


    def run_migrations(self):
        dir = './database/migration_scripts'
        for filename in os.listdir(dir):
            with open(f'{dir}/{filename}') as fileobj:
                self.execute(fileobj.read())

        self.commit()
