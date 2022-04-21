from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context

from resources.AutomatedMessages import automata

from dotenv import load_dotenv
from os import getenv

load_dotenv()

key = getenv('TONCENTERKEY')
TONCENTER_BASE_URL = "https://toncenter.com/api/v2"


class toggleVisibility(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='visibility', description='')
    async def toggle_prefix(self, ctx: Context):
        await self.toggleVis(ctx)

    async def toggleVis(self, ctx: Context):
        pass


def setup(bot):
    bot.add_cog(toggleVisibility(bot))
