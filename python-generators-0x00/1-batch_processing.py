from seed import connect_to_prodev

"""
a generator to fetch and process data in batches from the users database
"""

def stream_users_in_batches(batch_size):

    # Database connection
    
    connector = connect_to_prodev()
    mycursor = connector.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM user_data")
    
    while True:
        users_in_batch = mycursor.fetchmany(batch_size)
        if not users_in_batch:
            break  # Exitng the loop where there no more rows to be returned
        yield users_in_batch 
    
    mycursor.close()
    connector.close()

# Processing each batch of users and filtering users above 25

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        
        # Filtering users above 25
        filtered_batch = [user for user in batch if user['age'] > 25]
        
        for user in filtered_batch:
            print(user)
