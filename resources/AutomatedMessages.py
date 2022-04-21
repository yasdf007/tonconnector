# 'automata' is a discord embed script which creates nice messages within one command

# automata is created by bonzoteam and YET UNLICENSED
# the usage of it, therefore, is prohibited unless implemented by agreement with its original owners
# (c) Bonzoteam 2022

from discord import Embed
from discord import Colour


class automata:

    def generateEmbErr(x: str, error=None):
        result = Embed(
            title=f'**{x}**', color=Colour.red()
        )
        if error:
            readableErr = type(error).__name__
            result.set_footer(text=f'Error message / {readableErr}')
        else:
            result.set_footer(text='Error message')
        return result

    def generateEmbInfo(x: str):
        result = Embed(
            title=f'**{x}**',
            color=Colour.dark_green()
        )
        result.set_footer(text='bot message')
        return result
