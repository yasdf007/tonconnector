from discord.ext.commands import Cog, command, dm_only
from discord.ext.commands.context import Context
from discord.ext.commands.errors import MissingRequiredArgument, PrivateMessageOnly
from discord import Embed

from resources.AutomatedMessages import automata
from resources import walletChecker

from db import wallet

import random
import string
import aiohttp
import asyncio


TONCENTER_BASE_URL = "https://toncenter.com/api/v2"


class WalletConnect(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(embed=automata.generateEmbErr("Argument unspecified. Check command syntax => `verif help`", error=error))
        if isinstance(error, PrivateMessageOnly):
            return await ctx.send(embed=automata.generateEmbErr("You may only use this by DM'ing the bot.", error=error))

        raise error

    @dm_only()
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

        if await wallet.getWallet(self.bot.database, ctx.author.id) != None:
            await ctx.send("Wallet is already tethered, proceed if you want to tether another wallet.")

        params = {"address": address, "api_key": self.bot.ton_api_key}

        if await walletChecker.isValid(address):
            embed = Embed('Wallet found on TON :white_check_mark:')
            embed.add_field(name='Follow the instructions!',
                            value="You have 5 minutes to commit the transaction to your wallet (to self) with details specified below")
            await ctx.send(embed=embed)
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
                await ctx.send(embed=automata.generateEmbErr("An unexpected error occurred. Operation cancelled."))
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
            if not await wallet.insertUserWallet(self.bot.database, ctx.author.id, address):
                await wallet.updateWallet(self.bot.database, ctx.author.id, address)

            result = Embed(title='SUCCESS :white_check_mark:')
            result.add_field(
                name=f'{ctx.author},', value=f'Your wallet `{address}` is tethered to Yout user id! (`{ctx.author.id}`)', inline=False)
            await ctx.send(embed=result)
        else:
            result = Embed(title='FAIL :x:')
            result.add_field(
                name=f'{ctx.author},', value=f'unfortunately, Your wallet verification failed. Please contact project support if You need any assistance.', inline=False)
            await ctx.send(embed=result)


def setup(bot):
    bot.add_cog(WalletConnect(bot))


# class TonWallet:
#     address: str

#     def __init__(self, address: str) -> None:
#         self.address = address

#     async def getWalletInformation(self) -> str:
#         params = {"address": self.address}

#         async with aiohttp.ClientSession() as session:
#             async with session.get(TONCENTER_BASE_URL + '/getAddressInformation', params=params) as resp:
#                 res = await resp.json()
#         return res
