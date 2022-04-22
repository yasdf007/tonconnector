from WalletType import TonWallet as wallet

from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord.ext.commands.errors import MissingRequiredArgument
from discord import Embed

from resources.AutomatedMessages import automata

from db import dbQuery
from discord.member import Member

TONCENTER_BASE_URL = "https://toncenter.com/api/v2"


class GetInfo(Cog):
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
        walletInfo = await dbQuery.getWallet(self.bot.database, user.id)

        if walletInfo:
            if walletInfo["public"]:
                response = await wallet(walletInfo["address"]).getWalletInformation()

                embed = Embed(title="**User information**", color=0xff0000)
                embed.add_field(name="User:", value=user.mention, inline=False)
                embed.add_field(
                    name="Wallet:", value=f'`{walletInfo["address"]}`', inline=False)
                embed.add_field(
                    name="Balance:", value=f'{float(response["result"]["balance"])/10**9}:gem:', inline=False)
                embed.set_thumbnail(
                    url=user.avatar_url_as(static_format="png"))
                embed.set_footer(
                    text="TON Connector is in alpha. Proceed with caution.")

            else:
                embed = Embed(title="**User information**", color=0xff0000)
                embed.add_field(name="User:", value=user.mention, inline=False)
                embed.add_field(
                    name="Wallet:", value="verified and hidden :white_check_mark:", inline=False)
                embed.set_thumbnail(
                    url=user.avatar_url_as(static_format="png"))
                embed.set_footer(
                    text="TON Connector is in alpha. Proceed with caution.")

        else:
            embed = automata.generateEmbErr(
                f"User {user} has not verified their wallet yet. :x:")

        await ctx.send(embed=embed)

        @command(name='shareMy')
        async def shareMy_prefix(self, ctx: Context):
            await self.shareMy(ctx)

        async def shareMy(self, ctx: Context):
            walletInfo = await dbQuery.getWallet(self.bot.database, ctx.author.id)

            if walletInfo:

                embed = Embed(title="Secure wallet sharing:", color=0x26ff00)
                embed.add_field(
                    name=':white_check_mark', value=f'{ctx.author.mention} is confirmed owner of `{walletInfo["address"]}`')
                embed.set_footer(
                    f'Presented data is verified via TON Connector.')
                await ctx.send(embed=embed)

            else:
                await ctx.send(embed=automata.generateEmbErr(f"{ctx.author}, You haven't verified your wallet yet."))


def setup(bot):
    bot.add_cog(GetInfo(bot))
