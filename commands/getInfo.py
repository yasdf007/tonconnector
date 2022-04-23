from WalletType import TonWallet as wallet

from discord.ext.commands import Cog, command, guild_only, cooldown, BucketType
from discord.ext.commands.context import Context
from discord.ext.commands.errors import MissingRequiredArgument, CommandOnCooldown, NoPrivateMessage
from discord.member import Member
from discord import Embed

from resources.AutomatedMessages import automata

from db import dbQuery


class GetInfo(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            return await ctx.message.reply(embed=automata.generateEmbErr("Argument unspecified. Check command syntax => `verif help`", error=error))

        if isinstance(error, NoPrivateMessage):
            return await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "This command can only be used in server channel.", error=error
                )
            )
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "This command is on cooldown. Try again later.",
                    error=error,
                )
            )
        raise error

    @guild_only()
    @cooldown(rate=3, per=300, type=BucketType.user)
    @command(name='user', description='')
    async def getUser_prefix(self, ctx: Context, user: Member = None):
        if not ctx.guild:
            raise NoPrivateMessage
        if not user:
            user = ctx.author
        await self.getUser(ctx, user)

    async def getUser(self, ctx: Context, user: Member):
        await ctx.message.delete()
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

    @guild_only()
    @cooldown(rate=2, per=120, type=BucketType.user)
    @command(name='share')
    async def shareMy_prefix(self, ctx: Context):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.shareMy(ctx)

    async def shareMy(self, ctx: Context):
        await ctx.message.delete()
        walletInfo = await dbQuery.getWallet(self.bot.database, ctx.author.id)

        if walletInfo:

            embed = Embed(title="Secure wallet sharing:", color=0x26ff00)
            embed.add_field(
                name=':white_check_mark:', value=f'{ctx.author.mention} is confirmed owner of `{walletInfo["address"]}`')
            embed.set_footer(
                text=f'Presented data is verified via TON Connector.')
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=automata.generateEmbErr(f"{ctx.author}, You haven't verified your wallet yet."), delete_after=10)


def setup(bot):
    bot.add_cog(GetInfo(bot))
