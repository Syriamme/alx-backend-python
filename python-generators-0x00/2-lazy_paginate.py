from seed import connect_to_prodev

"""
fetching paginated data from the users database using a generator to lazily load each page
"""

def paginate_users(page_size, offset):

    connector = connect_to_prodev()


    mycursor = connector.cursor(dictionary=True)
    query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    
    
    mycursor.execute(query)
    users = mycursor.fetchall()  # Fetchng the rows


    mycursor.close()
    connector.close()

    return users

# Function for lazily paginating users data

def lazy_paginate(page_size):
    offset = 0

    while True:
        # Fetch the users for the current page
        users = paginate_users(page_size, offset)

        if not users:
            break  # Exit if no data is no longer returned

        yield users

        offset += page_size  # Updating offset for next page