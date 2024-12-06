import sqlite3
import functools

"""

Decorator handling database connection

"""

def with_db_connection(myfunc):
    @functools.wraps(myfunc)
    def wrapper(*myargs, **mykwargs):
        
        # Open database connection
        connection = sqlite3.connect('users.db')
        try:
            
            # Passing connection
            return myfunc(connection, *myargs, **mykwargs)
        finally:
            connection.close()
    
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
