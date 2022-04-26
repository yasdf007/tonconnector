from resources.WalletType import TonWallet
from resources.AutomatedMessages import automata
from resources.Errors import NoWalletFound, RequestError

from db import dbQuery

from discord.ext.commands import Cog, command, Context, cooldown, CommandOnCooldown, guild_only, BucketType, NoPrivateMessage
from discord import Embed


class Perks(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            return await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "This command is on cooldown. Try again later.",
                    error=error
                )
            )
        if isinstance(error, NoWalletFound):
            return await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "You haven't tethered your TON wallet yet.",
                    error=error
                )
            )
        if isinstance(error, RequestError):
            return await ctx.message.reply(
                embed=automata.generateEmbErr(
                    f"Data cannot be loaded. Contact bot support. :x:",
                    error=error
                )
            )
        if isinstance(error, NoPrivateMessage):
            return await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "This command can only be used in a server channel.",
                    error=error
                )
            )

        raise error

    @guild_only()
    @cooldown(rate=1, per=600, type=BucketType.user)
    @command(name='perkcheck')
    async def perkchecker_prefix(self, ctx: Context):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.perkcheck(ctx)

    async def perkcheck(self, ctx: Context):
        collectionDict = await dbQuery.getConnectedCollection(self.bot.database, ctx.guild.id)
        if not collectionDict:
            await ctx.message.reply(embed=automata.generateEmbErr("This server has no perks available via TON Connector."))
            return

        role = ctx.guild.get_role(collectionDict['role_id'])
        if role in ctx.author.roles:
            await ctx.message.reply(embed=automata.generateEmbErr(f"You have already obtained your NFT holder perks."))
            return

        walletInfo = await dbQuery.getWallet(self.bot.database, ctx.author.id)
        if not walletInfo:
            raise NoWalletFound

        wallet = TonWallet(walletInfo["address"])

        res = await self.bot.disintar_api.get_address_entities(wallet.address)

        if not res or not res['success']:
            raise RequestError

        if not res['data']:
            forms = await wallet.detectAddress(custDict=True)

            if not forms:
                raise RequestError

            res = await self.bot.disintar_api.get_address_entities(forms['nb64url'])

            if not res or not res['success']:
                raise RequestError

        if not res['data']:
            await ctx.send(embed=automata.generateEmbErr('No NFTs were found on your wallet. :x:'))
            return

        await ctx.message.delete()

        for nft in res['data']:
            if nft['collection']['address'] == collectionDict['collection_address']:
                await ctx.author.add_roles(role)
                embed = Embed(title='SUCCESS :white_check_mark:')
                embed.add_field(name='Perk received:',
                                value=f"You were given {role.mention} role!", inline=False)
                embed.add_field(name='For holding:',
                                value=f'{nft["name"]}', inline=False)
                await ctx.send(embed=embed)
                return

        await ctx.send(embed=automata.generateEmbErr("No eligible NFTs were found. :x:"))


def setup(bot):
    bot.add_cog(Perks(bot))
