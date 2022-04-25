from discord.ext.commands import CommandError


class NoWalletFound(CommandError):
    pass


class NotTONAddress(CommandError):
    pass
