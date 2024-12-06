import time
import sqlite3
import functools

"""

a decorator that retries database operations 
if they fail due to transient errors

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


# retry_on_failure decorator
def retry_on_failure(retries=3, delay=1):
    """
    Decorator for retrying a function on failure.
    """
    def decorator(myfunc):
        @functools.wraps(myfunc)
        def mywrapper(*myargs, **mykwargs):
            the_last_exception = None
            for attempt in range(retries):
                try:
                    return myfunc(*myargs, **mykwargs)
                except Exception as e:
                    the_last_exception = e 
                    print(f"Attempt {attempt + 1} failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            print(f"All {retries} attempts have failed. We are now raising last exception.")
            raise the_last_exception
        return mywrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


users = fetch_users_with_retry()