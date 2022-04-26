import aiohttp
import asyncio
from discord.ext import tasks

BASE_URL = "https://beta.disintar.io/api/"
ENTITIES_DATA_URL = BASE_URL + "get_entities/"


class DisintarAPI:
    def __init__(self):
        self.CSRFTOKEN = str()

    cookies = {'csrftoken': ''}

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'referrer-policy': 'same-origin',
        'Referer': 'https://beta.disintar.io/',
    }

    @tasks.loop(hours=1)
    async def getCSRF(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, headers=self.headers) as resp:
                self.CSRFTOKEN = resp.cookies['csrftoken'].value
                return

    async def get_address_entities(self, wallet: str) -> dict:
        wallet_data = f'{{"name":"owner__wallet_address","value":"{wallet}"}}'

        if not self.getCSRF.is_running():
            self.getCSRF.start()

        if not self.CSRFTOKEN:
            return {'success': False}

        self.headers['X-CSRFToken'] = self.CSRFTOKEN
        self.cookies['csrftoken'] = self.CSRFTOKEN

        data = {
            "entity_name": (None, "NFT"),
            "order_by": (None, '[]'),
            "filter_by": (None, f'[{wallet_data}]'),
            "limi": (None, None),
            "page": (None, 0),
            "request_time": (None, 'undefined')
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(ENTITIES_DATA_URL, data=data, headers=self.headers, cookies=self.cookies) as resp:
                    return await resp.json()
        except:
            return {'success': False}
