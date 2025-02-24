# Main bot executable
# (c) Bonzoteam 2022

from discord import Intents, Game, Status
from discord.ext.commands import Bot as defaultBot, Cog, CommandNotFound

from db import postgres

from dotenv import load_dotenv
from os import getenv, listdir

from resources.Disintario import DisintarAPI

load_dotenv()


class Bot(defaultBot):
    def __init__(self):
        intents = Intents.default()
        self.game = Game(f"=> verif help <=")
        self.disintar_api = DisintarAPI()

        super().__init__(
            command_prefix="verif ",
            help_command=None,
            intents=intents,
        )

    def Load(self):
        for filename in listdir("./commands"):
            if filename.endswith(".py"):
                self.load_extension(f"commands.{filename[:-3]}")

    def run(self):
        self.Load()
        super().run(getenv("TOKEN"))

    @Cog.listener()
    async def on_ready(self):
        self.database = await postgres.connectToDB()
        await self.change_presence(status=Status.online, activity=self.game)
        await self.disintar_api.getCSRF()
        print('done loading')

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            pass


if __name__ == "__main__":
    bot = Bot()
    bot.run()
