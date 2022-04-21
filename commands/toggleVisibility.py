from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context

from resources.AutomatedMessages import automata

from db import wallet

TONCENTER_BASE_URL = "https://toncenter.com/api/v2"


class ToggleVisibility(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='visibility', description='')
    async def toggle_prefix(self, ctx: Context):
        await self.toggleVis(ctx)

    async def toggleVis(self, ctx: Context):
        newVis, ok = await wallet.toggleWalletVisibility(self.bot.database, ctx.author.id)
        if not ok:
            await ctx.send("could not toggle wallet visibility")
            return

        await ctx.send(embed=automata.generateEmbInfo(f"Visibility changed to {'public' if newVis else 'private'}"))


def setup(bot):
    bot.add_cog(ToggleVisibility(bot))
