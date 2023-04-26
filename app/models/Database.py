import os
import sys
import mariadb

class Database:
    def __init__(self):
        self.pool = None

    def establish_connection(self):
        db_username = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_schema = os.getenv('DB_SCHEMA')
        try:
            conn = mariadb.connect(
                host=db_host,
                port= 3306,
                user=db_username,
                password=db_password,
                database=db_schema
            )
            if conn:
                self.pool = conn
                return self.pool
            else:
                print("Error: connection failed")
        except mariadb.Error as e:
            print(f"error connecting to mariadb platform: {e}")
            sys.exit(1)

    def get_db(self):
        if not self.pool:
            return self.establish_connection()
        return self.pool

    def close_connection(self):
        if self.pool:
            self.pool.close()


