from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandOnCooldown

from resources.AutomatedMessages import automata
from resources.Errors import NoWalletFound

from db import dbQuery


class ToggleVisibility(Cog):
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

    @cooldown(rate=2, per=300, type=BucketType.user)
    @command(name='visibility')
    async def toggle_prefix(self, ctx: Context):
        await self.toggleVis(ctx)

    async def toggleVis(self, ctx: Context):
        newVis, ok = await dbQuery.toggleWalletVisibility(self.bot.database, ctx.author.id)

        if not ok:
            raise NoWalletFound

        await ctx.message.delete()
        await ctx.send(embed=automata.generateEmbInfo(f"Visibility changed to `{'public' if newVis else 'private'}`"), delete_after=10)


def setup(bot):
    bot.add_cog(ToggleVisibility(bot))
