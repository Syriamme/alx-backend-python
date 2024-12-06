import sqlite3
from datetime import datetime  # Import datetime for timestamps

# Decorator to log SQL queries with timestamps
def log_queries(func):
    def wrapper(*args, **kwargs):
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Log the SQL query (assumes it's the first argument)
        query = args[0] if args else None
        if query:
            print(f"[{timestamp}] Executing query: {query}")
        # Execute the original function
        return func(*args, **kwargs)
    return wrapper

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
