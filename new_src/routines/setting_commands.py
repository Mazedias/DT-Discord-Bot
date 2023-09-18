import discord
from new_src.game.dataclasses import Guild
from new_src.storage.storage_api import add_competition
from new_src.game.gamehandler import Gamehandler


async def execute_add_competition(interaction: discord.Interaction, 
                                  gamehandler: Gamehandler, 
                                  guild_id: int,
                                  guild_lable: str):
    # Add guild to system
    new_guild = Guild(guild_id, guild_lable)
    add_competition(new_guild)
    gamehandler.add_guild(new_guild)

    # Send response message
    embed = discord.Embed(title="Command executed successfully")
    embed.set_author(name="Info")
    await interaction.response.send_message(embed=embed)


async def execute_stop_periodic_message(interaction: discord.Interaction):
    # TODO
    pass


async def execute_start_periodic_message(interaction: discord.Interaction):
    # TODO
    pass


async def execute_set_periodic_message_channel(interaction: discord.Interaction,
                                               channel_id: int):
    # TODO
    pass
