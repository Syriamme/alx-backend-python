import csv
import uuid
import mysql.connector
from mysql.connector import Error

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
    

def create_db(connection):
    try:
        mycursor = connection.cursor()
        mycursor.execute("CREATE DATABASE FNOT EXISTS ALX_prodev")
        print("This database already exists")
    
    except Error as e:
        print(f"Error encoutered: {e}")


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
    try:
        cursor = connection.cursor()
        table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            age DECIMAL NOT NULL
        )
        """
        cursor.execute(table_query)
        print("user_data table has been created already.")
    except Error as e:
        print(f"Error when crerating the table: {e}")

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
                age = float(row['age'])  # Convert age to decimal
                
                # Check if the email already exists in the database
                cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result[0] > 0:
                    print(f"The email {email} already exists. Its time to skip.")
                    continue
                
                # Insert the data into the table
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