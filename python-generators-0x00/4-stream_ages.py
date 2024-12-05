from seed import connect_to_prodev
"""
a generator to compute a memory-efficient aggregate function i.e average age for a large dataset
"""

#function to stream ages
def stream_user_ages():
    connector = connect_to_prodev()
    mycursor = connector.cursor(dictionary=True)
    mycursor.execute("SELECT age FROM user_data")

    for row in mycursor:
        yield row['age']
    
    mycursor.close()

#function to calculate the average age

def calculate_average_age(connecting):
    total_for_age = 0
    total_count = 0

    for age in stream_user_ages(connecting):
        total_for_age += age
        total_count += 1
    
    if total_count > 0:
        average_age = total_for_age / total_count
        
        print(f"average users: {average_age}")
    else:
        print("No users found")
