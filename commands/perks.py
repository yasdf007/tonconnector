from resources.WalletType import TonWallet
from resources.AutomatedMessages import automata
from resources.Errors import NoWalletFound
from resources.Disintario import disintar

from db import dbQuery

from discord import Embed, Colour
from discord.ext.commands import Cog, command, Context, cooldown, CommandOnCooldown, guild_only, BucketType, NoPrivateMessage


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

    @guild_only
    @cooldown(rate=1, per=600, type=BucketType.user)
    @command(name='perkcheck')
    async def perkchecker_prefix(self, ctx: Context):
        if not ctx.guild:
            raise NoPrivateMessage
        await self.perkcheck(ctx)

    async def perkcheck(self, ctx: Context):
        walletInfo = await dbQuery.getWallet(self.bot.database, ctx.author.id)

        if walletInfo:
            wallet = TonWallet(walletInfo["address"])
            forms = wallet.detectAddress(custDict=True)

        else:
            raise NoWalletFound

# MIGHT BE IMPLEMENTED AS DISINTAR.ISITUSER(WALLET) AND TWO FORMS PASSED
        # for form in [forms[2], forms[4]]:
            # disintar scan if this wallet address form profile is found
        #    pass

        # IF NFT OF USER IS IN PERK VARS THEN GIVE ROLE ELSE NO PERKS FOUND.
