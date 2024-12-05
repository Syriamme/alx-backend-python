from connector import connect_db, create_database, connect_to_prodev, create_table, insert_data

def main():
    # Step 1: Connect to MySQL
    connecting = connect_db()
    if not connecting:
        return

    create_database(connection)

    connection.close()
    connection = connect_to_prodev()
    if not connection:
        return

    create_table(connection)

    data = "D:/alx-backend-python/python-generators-0x00/user_data.csv"

    insert_data(connection, data)

    connection.close()
    print("Setup and data insertion complete!")

if __name__ == "__main__":
    main()
