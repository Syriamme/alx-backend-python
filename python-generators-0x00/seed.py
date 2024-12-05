from connector import db_connection, create_db, connecting_prodev, create_table, insert_data

def main():
    # Step 1: Connect to MySQL
    connection = db_connection()
    if not connection:
        return

    # Step 2: Create the Database
    create_db(connection)

    # Step 3: Connect to ALX_prodev Database
    connection.close()  # Close the connection to reconnect to the specific database
    connection = connecting_prodev()
    if not connection:
        return

    # Step 4: Create Table
    create_table(connection)

    data = "D:\alx-backend-python\python-generators-0x00\user_data.csv"

    insert_data(connection, data)

        # Close the connection
    connection.close()
    print("Setup and data insertion complete!")

if __name__ == "__main__":
    main()
