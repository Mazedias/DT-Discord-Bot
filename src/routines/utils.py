import discord
import datetime

IN_PROCESS_EMBED = discord.Embed(title="Working...",
                                 description="I'm processing your request an will edit this message once i'm done!",
                                 colour=0x1a5fb4,
                                 timestamp=datetime.datetime.now())

BASIC_ERROR_EMBED = discord.Embed(title="Error...",
                                  description="A fatal error occured! Please contact the maintainer of this bot!",
                                  colour=0xe01b24,
                                  timestamp=datetime.datetime.now())

MISSING_PERMISSION_EMBED = discord.Embed(title="Error...",
                                         description="You need the 'Botadmin' role to execute this command!",
                                         colour=0xe01b24,
                                         timestamp=datetime.datetime.now())

UNDER_CONSTRUCTION_EMBED = discord.Embed(title="Information",
                                         description="This command is currently under construction!",
                                         colour=0xff7800,
                                         timestamp=datetime.datetime.now())

GMC_ID = 75
DAD_ID = 1
PCZ_ID = 271

def get_detailed_error_embed(message: str) -> discord.Embed:
    return discord.Embed(
        title="Error...",
        description="A error eccured!\n Error: {message}".format(message=message),
        colour=0xe66100,
        timestamp=datetime.datetime.now()
    )


def get_simple_message_embed(title: str, message: str) -> discord.Embed:
    return discord.Embed(
        title=title,
        description=message,
        colour=0x395f13,
        timestamp=datetime.datetime.now()
    )


def get_success_message() -> discord.Embed:
    return get_simple_message_embed("Success!", "The operation executed successful.")


def get_detailed_embed(title: str, description: str, fields: list[tuple[str, str]]) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x395f13,
        timestamp=datetime.datetime.now()
    )

    for field in fields:
        embed.add_field(
            name=field[0],
            value=field[1],
            inline=False
        )

    return embed