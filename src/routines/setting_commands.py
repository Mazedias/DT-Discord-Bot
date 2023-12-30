import discord
import storage.logging_config as logger

from routines.utils import IN_PROCESS_EMBED
from routines.utils import get_success_message, get_detailed_embed, get_detailed_error_embed
from game.dataclasses import Guild, Player
from storage.storage_api import add_competition, get_guild, load_competition, load_players
from storage.data_api import get_players

logger = logger.logger

async def execute_add_competition(interaction: discord.Interaction, 
                                  guild_id: int,
                                  guild_lable: str):
    logger.info(f"execute_add_competition' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)
    
    for guild in load_competition():
        if guild_id == guild.id:
            await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(f"Competition guild with id {guild_id} is alredy stored!"))
            logger.error(f"'execute_add_competition' failed because a guild with id {guild_id} is already stored.")
            return

    new_guild = Guild(guild_id, guild_lable)
    add_competition(new_guild)

    await interaction.edit_original_response(content=None, embed=get_success_message())


async def execute_botstatus(interaction: discord.Interaction):
    logger.info(f"execute_add_competition' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)
    
    home_guild: Guild = get_guild()
    competition: list[Guild] = load_competition()
    players: list[Player] = load_players()


    # Check if a player is not linked or if a link is outdated
    member_ingame_names = get_players(get_guild().id)
    outdated_player_links: list[Player] = []
    for p in players:
        if p.ingame_name not in member_ingame_names:
            outdated_player_links.append(p)
            continue
        member_ingame_names.remove(p.ingame_name)
    

    # Build messages
    competition_str = ""
    for comp in competition:
        competition_str += f"**Lable:** {comp.lable}   ---   **ID:** {comp.id}\n"
    outdated_member_str = ""
    for p in outdated_player_links:
        outdated_member_str += f"**Name:** {p.ingame_name}   ---   **Discord:** {p.discord_id}\n"
    unlinked_member_str = ""
    for p in member_ingame_names:
        unlinked_member_str += f"{p}\n"
    
    answer_embed = get_detailed_embed(
        "Status message",
        f"This Bot is configured for the guild with id: {home_guild.id} and lable: {home_guild.lable}",
        fields=[
            ("Configured competitions", competition_str),
            ("Outdated member links", outdated_member_str),
            ("Unlinked members", unlinked_member_str)
        ]
    )

    await interaction.edit_original_response(content=None, embed=answer_embed)


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
