import aiohttp
from dotenv import load_dotenv
from os import getenv

load_dotenv()

key = getenv('TONCENTERKEY')
TONCENTER_BASE_URL = "https://toncenter.com/api/v2"


async def isValid(address: str) -> bool:
    """performs checking whether the given address is valid or not.

    Args:
        address (str): TON Wallet Address

    Returns:
        bool: True if address is valid, False otherwise
    """
    params = {"address": address, "api_key": key}

    if not len(address) == 48:
        return False

    async with aiohttp.ClientSession() as session:
        async with session.get(TONCENTER_BASE_URL + '/getAddressInformation', params=params) as resp:
            res = await resp.json()

    return res["ok"]
