from seed import connect_to_prodev

"""
a generator to fetch and process data in batches from the users database
"""

def stream_users():
    connector = connect_to_prodev()
    mycursor = connector.cursor(dictionary=True)
    try:
        # Executing the SQL query
        mycursor.execute("SELECT * FROM user_data")
        rows = list(mycursor)
        for row in rows:
            yield row
    except Exception as e:
        print(f"Error: {e}")

    # closing the connection and mycursor
    finally:
        mycursor.close()
        connector.close()