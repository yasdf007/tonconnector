from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord.ext.commands.errors import MissingRequiredArgument
from discord import Embed

from resources.AutomatedMessages import automata

import aiohttp

from db import wallet
from discord.member import Member

from dotenv import load_dotenv
from os import getenv

load_dotenv()

key = getenv('TONCENTERKEY')
TONCENTER_BASE_URL = "https://toncenter.com/api/v2"


class getInfo(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(embed=automata.generateEmbErr("Argument unspecified. Check command syntax => `verif help`", error=error))

        raise error

    @command(name='user', description='')
    async def getUser_prefix(self, ctx: Context, user: Member):
        await self.getUser(ctx, user)

    async def getUser(self, ctx: Context, user: Member):
        addr = wallet.getWallet(self.pool, user.id)
        if not addr:
            await ctx.send("User has no wallet connected.")

        data = ''
        isPublic = True

        params = {"address": addr, "api_key": key}
        if user in data:

            if isPublic:

                async with aiohttp.ClientSession() as session:
                    async with session.get(TONCENTER_BASE_URL + '/getWalletInformation', params=params) as resp:
                        response = await resp.json()

                embed = Embed(title="**User information**", color=0xff0000)
                embed.add_field(name="User:", value=user, inline=False)
                embed.add_field(name="Wallet", value=addr, inline=False)
                embed.add_field(
                    name="Balance", value=float(response["result"]["balance"])/10**9, inline=False)
                embed.set_thumbnail(
                    url=user.avatar_url_as(static_format="png"))
                embed.set_footer(
                    text="TON Connector is in alpha. Proceed with caution.")

            else:
                embed = Embed(title="**User information**", color=0xff0000)
                embed.add_field(name="User:", value=user, inline=False)
                embed.add_field(
                    name="Wallet", value="verified and hidden :white_check_mark:", inline=False)
                embed.set_thumbnail(
                    url=user.avatar_url_as(static_format="png"))
                embed.set_footer(
                    text="TON Connector is in alpha. Proceed with caution.")

        else:
            embed = automata.generateEmbErr(
                f"User {user} has not verified their wallet yet.")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(getInfo(bot))
