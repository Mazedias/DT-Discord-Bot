import discord

import storage.logging_config as logger
from game.dataclasses import Player
from storage.storage_api import add_player, remove_player, load_players
from routines.utils import IN_PROCESS_EMBED
from routines.utils import get_success_message, get_detailed_error_embed

logger = logger.logger

async def execute_link_member(interaction: discord.Interaction,
                              ingame_name: str,
                              discord_name: str):
    logger.info(f"execute_link_member' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    player = Player(ingame_name, discord_name, True, True)

    try:
        add_player(player)
    except KeyError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "For this player a discord account is already linked!"
        ))
        logger.error(f"'execute_save_event' failed because the mapping for this ingame player already exists")
        return

    await interaction.edit_original_response(content=None, embed=get_success_message())


async def execute_remove_member(interaction: discord.Interaction,
                                ingame_name: str):
    logger.info(f"'execute_remove_member' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    # TODO

    try:
        remove_player(ingame_name)
    except KeyError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "Member was not found!"
        ))
        logger.error(f"'execute_save_event' failed because no member '{ingame_name}' was found to remove")
        return

    await interaction.edit_original_response(content=None, embed=get_success_message())


async def execute_temp_ping_avoid(interaction: discord.Interaction,
                                  ingame_name: str):
    logger.info(f"'execute_temp_ping_avoid' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    players: list[Player] = load_players()
    target: Player = None

    for player in players:
        if player.ingame_name == ingame_name:
            target = player
            break
        
    if target == None:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "Member was not found!"
        ))
        logger.error(f"'execute_temp_ping_avoid' failed because no member '{ingame_name}' was found")
        return

    player.temp_ping = False

    try:
        remove_player(player.ingame_name)
        add_player(player)
    except KeyError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "Member was not found!"
        ))
        logger.error(f"'execute_temp_ping_avoid' failed with error {e}")
        return

    await interaction.edit_original_response(content=None, embed=get_success_message())


async def execute_perma_ping_avoid(interaction: discord.Interaction,
                                   ingame_name: str):
    logger.info(f"'execute_perma_ping_avoid' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    players: list[Player] = load_players()
    target: Player = None

    for player in players:
        if player.ingame_name == ingame_name:
            target = player
            break
        
    if target == None:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "Member was not found!"
        ))
        logger.error(f"'execute_perma_ping_avoid' failed failed because no member '{ingame_name}' was found")
        return

    player.perma_ping = False

    try:
        remove_player(player.ingame_name)
        add_player(player)
    except KeyError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "Member was not found!"
        ))
        logger.error(f"'execute_perma_ping_avoid' failed failed because no member '{ingame_name}' was found")
        return

    await interaction.edit_original_response(content=None, embed=get_success_message())


async def execute_ping_again(interaction: discord.Interaction,
                             ingame_name: str):
    logger.info(f"'execute_ping_again' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    players: list[Player] = load_players()
    target: Player = None

    for player in players:
        if player.ingame_name == ingame_name:
            target = player
            break
        
    if target == None:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "Member was not found!"
        ))
        logger.error(f"'execute_ping_again' failed failed because no member '{ingame_name}' was found")
        return

    player.temp_ping = True
    player.perma_ping = True

    try:
        remove_player(player.ingame_name)
        add_player(player)
    except KeyError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "Member was not found!"
        ))
        logger.error(f"'execute_ping_again' failed failed because no member '{ingame_name}' was found")
        return

    await interaction.edit_original_response(content=None, embed=get_success_message())