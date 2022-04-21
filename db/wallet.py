import asyncpg


async def getWallet(pool: asyncpg.Pool, userId: int):
    query = "select address, public from user_wallet where user_id = $1"
    return await pool.fetchrow(query, userId)


async def insertUserWallet(pool: asyncpg.Pool, userId: int, walletAddress: str) -> bool:
    if await getWallet(pool, userId) != None:
        return False

    query = "insert into user_wallet(user_id, address) values($1, $2);"
    await pool.execute(query, userId, walletAddress)
    return True