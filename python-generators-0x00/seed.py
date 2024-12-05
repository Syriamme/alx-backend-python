import csv
import uuid
import mysql.connector
from mysql.connector import Error

"""
a generator that streams rows from an SQL database one by one
"""

def connect_db():
    try:
        connecting =mysql.connector.connect(
            host="localhost",
            user="root",
            password="Roniel@123"
        )
        return connecting

    except Error as e:
        print(f"Error while connecting to Msql server: {e}")
        return None
    

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()

def connect_to_prodev():
    try:
        connecting =mysql.connector.connect(
            host="localhost",
            user="root",
            password="Roniel@123",
            database = "ALX_prodev"
        )
        if connecting.is_connected():
            print("Sccessfully connected.")
        return connecting

    except Error as e:
        print(f"Error while connecting to Msql server: {e}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    try:
        # Correct SQL to create the user_data table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL
        );
        """
        cursor.execute(create_table_query)
        print("Table 'user_data' created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error when creating the table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        
        with open(data, mode="r") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # UUID for user_id
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = int (row['age'])
                
                # Check the email already exists in database
                cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result[0] > 0:
                    print(f"The email {email} already exists. Its time to skip.")
                    continue
                
                # Insert data into the table
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
                print(f"Record inserted: {name}, {email}, {age}")
        
        # Commit
        connection.commit()
        print("insertion complete.")
    
    except Error as e:
        print(f"Error while inserting data: {e}")
        connection.rollback()
    
    finally:
        if cursor:
            cursor.close()