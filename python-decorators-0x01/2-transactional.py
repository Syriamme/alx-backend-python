import sqlite3
import functools

"""

create a decorator that manages database transactions by 
automatically committing or rolling back changes

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

# Decorator for handling database transactions
def transactional(myfunc):
    @functools.wraps(myfunc)
    def mywrapper(connection, *myargs, **mykwargs):
        try:
            
            myresult = myfunc(connection, *myargs, **mykwargs)
            # Committing transaction if no errors happens
            connection.commit()
            return myresult
        except Exception as e:
            # Rolling back the transaction after error
            connection.rollback()
            print(f"Failed transaction and rolled back: {e}")
            raise
    return mywrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully.")
except Exception as e:
    print(f"Failed to update email: {e}")
