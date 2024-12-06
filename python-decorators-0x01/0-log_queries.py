import sqlite3
import functools
from datetime import datetime

"""
writing a decorator log_queries that logs the SQL query before executing it.

Prototype: def log_queries()
"""

#a the decorator log queries
def log_queries(func):
    @functools.wraps(func)
    def mywrapper(*myargs, **mykwargs):
        timestp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        thequery = myargs[0] if myargs else None
        if thequery:
            print(f"[{timestp}] Executing my query: {thequery}")

        return func(*myargs, **mykwargs)
    return mywrapper

##fetch_all_users is being decorated by @log_queries

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
