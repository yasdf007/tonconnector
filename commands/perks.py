from resources.WalletType import TonWallet
from resources.AutomatedMessages import automata
from resources.Errors import NoWalletFound

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
            await ctx.send("This server is not connected to this bot")
            return

        role = ctx.guild.get_role(collectionDict['role_id'])
        if role in ctx.author.roles:
            await ctx.send(f"You already have this role {role.name}")
            return
        walletInfo = await dbQuery.getWallet(self.bot.database, ctx.author.id)
        if not walletInfo:
            raise NoWalletFound

        wallet = TonWallet(walletInfo["address"])

        res = await self.bot.disintar_api.get_address_entities(wallet.address)
        if not res['success']:
            await ctx.send("Could not fetch remote data")
            return
        
        if not res['data']:
            forms = await wallet.detectAddress(custDict=True)
            res = await self.bot.disintar_api.get_address_entities(forms['nb64url'])
            if not res['success']:
                await ctx.send("Could not fetch remote data")
                return
        
        if not res['data']:
            await ctx.send("No nft were found on your account")
            return

        for nft in res['data']:
            if nft['collection']['address'] == collectionDict['collection_address']:
                await ctx.author.add_roles(role)
                embed = Embed(title='123')
                embed.add_field(name='123',value=f"You were given role: {role.mention}")
                await ctx.send(embed=embed)
                return

        await ctx.send("No connected nft were found")
# MIGHT BE IMPLEMENTED AS DISINTAR.ISITUSER(WALLET) AND TWO FORMS PASSED
        # for form in [forms[2], forms[4]]:
            # disintar scan if this wallet address form profile is found
        #    pass

        # IF NFT OF USER IS IN PERK VARS THEN GIVE ROLE ELSE NO PERKS FOUND.

def setup(bot):
    bot.add_cog(Perks(bot))