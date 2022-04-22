import aiohttp
from os import getenv


class TonWallet():
    def __init__(self, address: str):
        self.address = address
        self.TONCENTER_BASE_URL = "https://toncenter.com/api/v2"
        self.TON_API_KEY = getenv('TONCENTERKEY')
        self.params = {"address": self.address, "api_key": self.TON_API_KEY}

    async def isValid(self) -> bool:
        """performs checking whether the given address is valid or not.

        Args:
            address (str): TON Wallet Address

        Returns:
            bool: True if address is valid, False otherwise
        """

        if not len(self.address) == 48:
            return False

        async with aiohttp.ClientSession() as session:
            async with session.get(self.TONCENTER_BASE_URL + '/getAddressInformation', params=self.params) as resp:
                res = await resp.json()

        return res["ok"]

    async def getWalletInformation(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(self.TONCENTER_BASE_URL + '/getWalletInformation', params=self.params) as resp:
                response = await resp.json()

        return response

    async def getTransactions(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(self.TONCENTER_BASE_URL + '/getTransactions', params=self.params) as resp:
                caught = await resp.json()

        return caught
