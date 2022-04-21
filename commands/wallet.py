from discord.ext.commands import Cog, command, CommandError
from discord.ext.commands.context import Context
from discord.ext.commands.errors import MissingRequiredArgument

from resources.AutomatedMessages import automata
from resources import walletChecker

import random
import string
import aiohttp
import asyncio


from dotenv import load_dotenv
from os import getenv

load_dotenv()

key = getenv('TONCENTERKEY')
TONCENTER_BASE_URL = "https://toncenter.com/api/v2"


class Wallet(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(embed=automata.generateEmbErr("Argument unspecified. Check command syntax => `verif help`", error=error))

        raise error

    @command(name='connect', description='')
    async def walletconn_prefix(self, ctx: Context, address: str):
        await self.walletconn(ctx, address)

    async def walletconn(self, ctx: Context, address: str):
        """initiates tethering wallet with specified address
           with discord user account

        Args:
            ctx (Context): discord.py Context class
            address (str): ton wallet address
        """

        await ctx.send(f"indev, working. spec address: {address}")
        params = {"address": address, "api_key": key}

        if await walletChecker.isValid(address):
            await ctx.send(embed=automata.generateEmbInfo("Wallet found on TON :white_check_mark:"))
            await ctx.send("You have 5 minutes to commit the transaction to your wallet (to self) with details specified below")

        else:
            await ctx.send(embed=automata.generateEmbErr("Wallet is either invalid or doesn't have recent transactions. :x:"))
            return

        letters = string.ascii_letters
        memo = ''.join(random.choice(letters) for _ in range(6))
        await ctx.send(f'{ctx.author.mention}, AMOUNT: `0.001 TON`, MEMO (COMMENT): `{memo}`')

        async def transactionCatcher():
            """This function checks whether requested transaction was sent

            Returns:
                bool: True if transaction found, False otherwise
            """
            async with aiohttp.ClientSession() as session:
                async with session.get(TONCENTER_BASE_URL + '/getTransactions', params=params) as resp:
                    caught = await resp.json()

            if not caught["ok"]:
                await ctx.send(f"{ctx.author.mention} an unexpected error occurred. Operation cancelled.")
                return

            for tx in caught["result"]:
                if tx["in_msg"]["message"] == memo and tx["in_msg"]["source"] == tx["in_msg"]["destination"] and tx["in_msg"]["value"] == "1000000":
                    return True

            return False

        # the following part requires rewriting using asyncio Tasks
        for _ in range(60*5//20):
            transaction = await transactionCatcher()
            if transaction == True:
                break
            await asyncio.sleep(20)

        if transaction:
            await ctx.send(embed=automata.generateEmbInfo("SUCCESS :white_check_mark:"))
            await ctx.send(f"""{ctx.author.mention}, wallet `{address}` is tethered to discord user id `{ctx.author.id}`!""")
        else:
            await ctx.send(embed=automata.generateEmbErr("FAIL :x:"))
            await ctx.send(
                f'{ctx.author.mention}, unfortunately, Your wallet verification failed. Please contact project support if You need any assistance.')

# CHECK FOR NFTS
    @command(name='scan', description='')
    async def walletcheck_prefix(self, ctx: Context, address: str):
        await self.walletcheck(ctx, address)

    async def walletcheck(self, ctx, address: str):
        query = f" "
        await ctx.send('RESULT')


def setup(bot):
    bot.add_cog(Wallet(bot))


class TonWallet:
    address: str

    def __init__(self, address: str) -> None:
        self.address = address

    async def getWalletInformation(self) -> str:
        params = {"address": self.address}

        async with aiohttp.ClientSession() as session:
            async with session.get(TONCENTER_BASE_URL + '/getAddressInformation', params=params) as resp:
                res = await resp.json()
        return res
