import aiosqlite
import asyncio

#asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("dental_clinic.db") as db:

        cursor = await db.execute("SELECT * FOM users")

        data = await cursor.fetchall()

        await cursor.close()
        
        for row in data:
            print(row)

#asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("dental_clinic.db") as db:

        cursor = await db.execute("SELECT * FOM users WHERE age > 20")

        data = await cursor.fetchall()

        await cursor.close()
        
        for row in data:
            print(row)

async def fetching_conc():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetching_conc())