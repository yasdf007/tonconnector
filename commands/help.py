from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord import Embed, Colour


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='help')
    async def help(self, ctx: Context):
        """This command returns an embed with bot usage instructions

        Args:
            ctx (Context): Discord context

        Returns:
            Embed: returns discord embed with help message
        """

        embed = Embed(title="**TON Connector**",
                      description="Usage instructions", color=Colour.dark_blue())
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/966617494708191252/69aa48df063ec479c242f08be9256d93.webp?size=240")
        embed.add_field(
            name="Connect", value="`verif connect [address]` - verifies and tethers Your TON Wallet to your Discord account", inline=False)
        embed.add_field(name="User information",
                        value="`verif user [@user]` - shows the information about user (whether he has verified wallet or not). Balance and full address available if user decides to toggle public visibility.", inline=False)
        embed.add_field(name="Public/Private visibility",
                        value="`verif visibility` - toggles your address visibility (public/private) [private by default]", inline=False)
        embed.set_footer(
            text="TON Connector is in alpha. Proceed with caution.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
