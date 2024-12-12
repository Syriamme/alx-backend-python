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

#Closes db connection if open
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Closed.")

    # Methodsfor context managers
    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()