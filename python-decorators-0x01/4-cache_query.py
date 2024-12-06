import sqlite3
import functools

"""
Decorator to cache query results based on the query string.
"""

#Store query results as cache
cache = {}

# cache_query decorator
def cache_query(func):

    @functools.wraps(func)
    def wrapper(*myargs, **mykwargs):
        myquery = mykwargs.get("query") or (myargs[1] if len(myargs) > 1 else None)

        if myquery in cache:
            print("Using cached result for query:", myquery)
            return cache[myquery]  # Return cached result
        
        # If not in cache, execute the function and store the result in cache
        myresult = func(*myargs, **mykwargs)
        cache[myquery] = myresult  # Cache the result

        print("Caching result for query:", myquery)
        return myresult
    return wrapper

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
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


users = fetch_users_with_cache(query="SELECT * FROM users")
