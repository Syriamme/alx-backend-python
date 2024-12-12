import mysql.connector
from mysql.connector import Error

"""
a class based context manager to handle opening and closing database connections automatically
"""

#initiliazing connection parameters

class  ExecuteQuery:
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
                self.cursor = self.connection.cursor()
            
        except Error as e:
            print(f"Error trying connecting to: {e}")
            self.connection = None
            raise
        return self
    
    def execute_query(self, qry, param=None):
        try:
            self.cursor.execute(qry, param)
            return self.cursor.fetchall()
        except Error as e:
            return []
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Closed.")

    # Methodsfor context managers
    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

#Context manager and the SELECT Query
def query_database():
    qry = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    
    with ExecuteQuery("localhost", "root", "Roniel@123", "dental_clinic") as db_manager:
        results = db_manager.execute_query(qry, param)
        print("Query Results:")
        for row in results:
            print(row)