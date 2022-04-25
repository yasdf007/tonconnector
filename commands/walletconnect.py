from resources.WalletType import TonWallet as wallet

from discord.ext.commands import Cog, command, dm_only, BucketType, cooldown, CommandOnCooldown
from discord.ext.commands.context import Context
from discord.ext.commands.errors import MissingRequiredArgument, PrivateMessageOnly
from discord import Embed, File

from db import dbQuery
from resources.AutomatedMessages import automata

import random
import string
import asyncio
import qrcode
from io import BytesIO


class WalletConnect(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            return await ctx.message.reply(embed=automata.generateEmbErr("Argument unspecified. Check command syntax => `verif help`", error=error), delete_after=10)
        if isinstance(error, PrivateMessageOnly):
            await ctx.message.delete()
            return await ctx.send(embed=automata.generateEmbErr("You may only connect Your wallet by using direct messages. This is made to keep your data private and secured.", error=error), delete_after=10)
        if isinstance(error, CommandOnCooldown):
            return await ctx.message.reply(embed=automata.generateEmbErr("In order to avoid overloading we have set 6 minutes long cooldown on this command. Try again later.", error=error))

        raise error

    @dm_only()
    @cooldown(rate=1, per=360, type=BucketType.user)
    @command(name='connect', description='')
    async def walletconn_prefix(self, ctx: Context, address: str):
        await self.walletconn(ctx, address)

    async def walletconn(self, ctx: Context, address: str):
        """initiates tethering wallet with specified address
           with discord user account

        Args:
            ctx (Context): discord.py Context class
            address (str): ton wallet address (any form)
        """

        if await wallet(address).isValid():
            addrForms = await wallet(address).detectAddress(custDict=True)
            address = addrForms['standard']

            if await dbQuery.getWallet(self.bot.database, ctx.author.id) != None:
                await ctx.send(embed=automata.generateEmbInfo("Wallet is already tethered, proceed ONLY if you want to tether another wallet :exclamation:"))

            embed = Embed(title='Wallet found on TON :white_check_mark:')
            embed.add_field(name='Follow the instructions!',
                            value="You have 5 minutes to commit the transaction to your wallet (to self) with details specified below")
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=automata.generateEmbErr("Wallet is either invalid or not initialized. :x:"))
            return

        letters = string.ascii_letters
        memo = ''.join(random.choice(letters) for _ in range(6))
        requiredTransaction = Embed(
            title='Make a transaction with following parameters:')
        requiredTransaction.add_field(
            name='AMOUNT:', value=f'`0.001`:gem:', inline=False)
        requiredTransaction.add_field(
            name='RECIPIENT:', value=f'`{address}`', inline=False)
        requiredTransaction.add_field(
            name='MEMO (COMMENT):', value=f'`{memo}`', inline=False)

        qrlink = f'ton://transfer/{address}?amount={0.001* 10**9}&text={memo}'
        img = qrcode.make(qrlink)

        with BytesIO() as temp:
            img.save(temp, "png")
            temp.seek(0)
            file = File(fp=temp, filename="qr.png")
            requiredTransaction.set_image(url="attachment://qr.png")
            await ctx.send(file=file, embed=requiredTransaction)

        async def transactionCatcher():
            """This function checks whether requested transaction was sent

            Returns:
                bool: True if transaction found, False otherwise
            """

            caught = await wallet(address).getTransactions()

            if not caught["ok"]:
                caught = await wallet(address).getTransactions(archiveNode=True)
                if not caught["ok"]:
                    await ctx.send(embed=automata.generateEmbErr("An unexpected error occurred. Operation cancelled."))
                    return "Err"

            for tx in caught["result"]:
                if tx["in_msg"]["message"] == memo and tx["in_msg"]["source"] == tx["in_msg"]["destination"] and tx["in_msg"]["value"] == "1000000":
                    return True

            return False

        # the following part requires rewriting using asyncio Tasks
        for _ in range(60*5//20):
            transaction = await transactionCatcher()

            if transaction:
                break

            await asyncio.sleep(20)

        if transaction == True:
            if not await dbQuery.insertUserWallet(self.bot.database, ctx.author.id, address):
                await dbQuery.updateWallet(self.bot.database, ctx.author.id, address)

            result = Embed(title='SUCCESS :white_check_mark:')
            result.add_field(
                name=f'{ctx.author},', value=f'Your wallet `{address}` is tethered to Your user id! (`{ctx.author.id}`)', inline=False)
            await ctx.send(embed=result)
        else:
            result = Embed(title='FAIL :x:')
            result.add_field(
                name=f'{ctx.author},', value=f'unfortunately, Your wallet verification failed. Please contact project support if You need any assistance.', inline=False)
            await ctx.send(embed=result)


def setup(bot):
    bot.add_cog(WalletConnect(bot))
