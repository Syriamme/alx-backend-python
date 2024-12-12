import mysql.connector
from mysql.connector import Error

"""
a class based context manager to handle opening and closing database connections automatically
"""

#initiliazing connection parameters

class DatabaseConnection:
    def __init__(self, ht, usr, pswd, db):
        self.ht = ht
        self.usr = usr
        self.pswd = pswd
        self.db = db
        self.connection = None

#connecting to the database
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                ht=self.ht,
                usr=self.usr,
                psd=self.pswd,
                db=self.db
            )
            if self.connection.is_connected():
                print("Connected successfully the database.")
        except Error as e:
            print(f"Error trying connecting to: {e}")
            self.connection = None
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Closed.")

    # Methodsfor context managers
    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

#Context manager and the SELECT Query
def query_database():
    query = "SELECT * FROM user_data"
    
    with DatabaseConnection("localhost", "root", "Roniel@123", "ALX_prodev") as connection:
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
            cursor.close()

query_database()