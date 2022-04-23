from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.ext.commands.context import Context

from resources.AutomatedMessages import automata

from db import dbQuery


class ToggleVisibility(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(rate=2, per=300, type=BucketType.user)
    @command(name='visibility', description='')
    async def toggle_prefix(self, ctx: Context):
        await self.toggleVis(ctx)

    async def toggleVis(self, ctx: Context):
        newVis, ok = await dbQuery.toggleWalletVisibility(self.bot.database, ctx.author.id)
        if not ok:
            await ctx.send("could not toggle wallet visibility")
            return

        await ctx.send(embed=automata.generateEmbInfo(f"Visibility changed to {'public' if newVis else 'private'}"))


def setup(bot):
    bot.add_cog(ToggleVisibility(bot))
