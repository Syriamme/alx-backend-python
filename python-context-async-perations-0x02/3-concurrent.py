import aiosqlite
import asyncio

#asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("dental_clinic.db") as db:

        cursor = await db.execute("SELECT * FOM users")

        data = await cursor.fetchall()

        await cursor.close()

        return data

#asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("dental_clinic.db") as db:

        cursor = await db.execute("SELECT * FOM users WHERE age > 20")

        data = await cursor.fetchall()

        await cursor.close()
        
        return data

async def fetch_concurrently():
    all_usrs, older_usrs = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:")
    for row in all_usrs:
        print(row)
    
    
    print("\n All users that are Older than 40:")
    for row in older_usrs:
        print(row)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())