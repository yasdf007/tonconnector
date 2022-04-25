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

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.TONCENTER_BASE_URL + '/getAddressInformation', params=self.params) as resp:
                    res = await resp.json()

            return res["ok"]

        except:
            return False

    async def getWalletInformation(self) -> dict:
        """Gets wallet information as provided by toncenter API v2

        Returns:
            dict: json-response of toncenter api
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.TONCENTER_BASE_URL + '/getWalletInformation', params=self.params) as resp:
                    response = await resp.json()

            return response
        except:
            return False

    async def getTransactions(self, archiveNode=False) -> dict:
        """Gets transactions as provided by toncenter API v2

        Returns:
            dict: json-response of toncenter api
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.TONCENTER_BASE_URL + '/getTransactions', params=self.params | {"archival": f'{archiveNode}'}) as resp:
                    response = await resp.json()

            return response

        except:
            return False

    async def detectAddress(self, custDict=False) -> dict:

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.TONCENTER_BASE_URL + '/detectAddress', params=self.params) as resp:
                    response = await resp.json()

            if not custDict:
                return response

            return {'raw': response["result"]["raw_form"],
                    'bb64': response["result"]["bounceable"]["b64"],
                    'standard': response["result"]["bounceable"]["b64url"],
                    'nb64': response["result"]["non_bounceable"]["b64"],
                    'nb64url': response["result"]["non_bounceable"]["b64url"]
                    }
        except:
            return False
