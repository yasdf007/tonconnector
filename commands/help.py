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
            name="Connect", value="`verif connect [address]` - verifies and tethers your TON wallet address to your Discord account. Usage only allowed in DMs to avoid any unexpected data leak. CryptoBot and outher custodial wallets are unacceptable.", inline=False)
        embed.add_field(name="User information",
                        value="`verif user [@user]` - shows the information about user (whether he has verified wallet or not). Balance and full address available if user decides to toggle public visibility.", inline=False)
        embed.add_field(
            name="Check for perks", value="`verif perkcheck` - checks if you're eligible for any NFT holder role and grants it if its available.", inline=False)
        embed.add_field(name="Public/Private visibility",
                        value="`verif visibility` - toggles your address visibility in user information. (public/private) [private by default]", inline=False)
        embed.add_field(name="Address sharing",
                        value="`verif share` - sends your wallet address to current channel. THINK TWICE BEFORE USING!")
        embed.add_field(
            name=':superhero:', value="**[Click here to join developer/support server!](https://discord.gg/4H9j5mVhgN)**", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
