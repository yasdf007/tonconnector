import asyncpg


async def getWallet(pool: asyncpg.Pool, userId: int):
    query = "select address, public from user_wallet where user_id = $1"
    return await pool.fetchrow(query, userId)


async def updateWallet(pool: asyncpg.Pool, userId: int, walletAddress: str):
    query = "update user_wallet set address = $1 where user_id = $2"
    return await pool.execute(query, walletAddress, userId)


async def toggleWalletVisibility(pool: asyncpg.Pool, userId: int):
    walletInfo = await getWallet(pool, userId)
    if not walletInfo:
        return False, False

    query = "update user_wallet set public = $1 where user_id = $2"
    await pool.execute(query, True if not walletInfo["public"] else False, userId)

    return True if not walletInfo["public"] else False, True


async def insertUserWallet(pool: asyncpg.Pool, userId: int, walletAddress: str) -> bool:
    if await getWallet(pool, userId) != None:
        return False

    query = "insert into user_wallet(user_id, address) values($1, $2);"
    await pool.execute(query, userId, walletAddress)
    return True

async def getConnectedCollection(pool: asyncpg.Pool, server_id: int):
    query = "SELECT NFTS.collection_address, NFTS.collection_name, role_id from connected_servers join NFTS on connected_servers.nft_id=NFTS.id where server_id = $1;"

    return await pool.fetchrow(query, server_id)
