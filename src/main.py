import discord
from discord import app_commands
import traceback

import storage.logging_config as logger
import storage.storage_api as storage
from storage import *
from routines.event_commands import execute_summary, execute_overview, execute_eventdata, execute_new_event, execute_save_event, execute_iteminfo
from routines.member_commands import execute_link_member, execute_remove_member, execute_temp_ping_avoid, execute_perma_ping_avoid, execute_ping_again
from routines.setting_commands import execute_add_competition, execute_set_periodic_message_channel, execute_botstatus
from routines.utils import MISSING_PERMISSION_EMBED

# Initiating discord bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)

# Setup logger
logger = logger.logger

# Startup message
@client.event
async def on_ready():
    print("Bot is up and running")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# Registrate all commands
@tree.command(name="summary", description="Status report of the event")
async def summary(interaction: discord.Interaction):
    await execute_summary(interaction)


@tree.command(name="overview", description="Inforamtions about the last events")
async def overview(interaction: discord.Integration):
    await execute_overview(interaction)


@tree.command(name="eventdata", description="Inforamtions about the last event")
async def eventdata(interaction: discord.Integration):
    await execute_eventdata(interaction)


@tree.command(name="newevent", description="Create a new event")
@app_commands.describe(event_round="Round")
@app_commands.describe(item1="Item 1")
@app_commands.describe(amount1="Amount Item 1")
@app_commands.describe(item2="Item 2")
@app_commands.describe(amount2="Amount Item 2")
@app_commands.describe(item3="Item 3")
@app_commands.describe(amount3="Amount Item 3")
@app_commands.describe(item4="Item 4")
@app_commands.describe(amount4="Amount Item 4")
async def new_event(interaction: discord.Interaction,
                   event_round: str,
                   item1: str, amount1: str,
                   item2: str, amount2: str,
                   item3: str, amount3: str,
                   item4: str, amount4: str):
    await execute_new_event(
        interaction, event_round,
        item1, amount1,
        item2, amount2,
        item3, amount3,
        item4, amount4
    )


@tree.command(name="saveevent", description="Store data of the last event")
async def save_event(interaction: discord.Interaction):
    await execute_save_event(interaction)


@tree.command(name="iteminfo", description="Shows amount of needed items")
@app_commands.describe(start="Start round")
@app_commands.describe(end="End round")
async def iteminfo(interaction: discord.Interaction, start:int, end: int): 
    await execute_iteminfo(interaction, start, end)


@tree.command(name="linkmember", description="Link a guild member to a discord account")
@app_commands.describe(ingame_name="Ingame name of the member")
@app_commands.describe(discord_name="Discord name of the member")
@app_commands.checks.has_role("Botadmin")
async def link_member(interaction: discord.Interaction,
                      ingame_name: str,
                      discord_name: str):
    await execute_link_member(interaction, ingame_name, discord_name)


@tree.command(name="removemember", description="Removes the link between a guild member and a discord account")
@app_commands.describe(ingame_name="Ingame name of the member")
@app_commands.checks.has_role("Botadmin")
async def remove_member(interaction: discord.Interaction, ingame_name: str):
    await execute_remove_member(interaction, ingame_name)


@tree.command(name="avoidtemp", description="Prevents a player from getting pinged for one event")
@app_commands.describe(ingame_name="Ingame name of the member")
@app_commands.checks.has_role("Botadmin")
async def temp_ping_avoid(interaction: discord.Interaction, ingame_name: str):
    await execute_temp_ping_avoid(interaction, ingame_name)


@tree.command(name="avoidperma", description="Prevents a player from getting pinged permanently")
@app_commands.describe(ingame_name="Ingame name of the member")
@app_commands.checks.has_role("Botadmin")
async def perma_ping_avoid(interaction: discord.Interaction, ingame_name: str):
    await execute_perma_ping_avoid(interaction, ingame_name)


@tree.command(name="pingagain", description="Activates all pings for player again")
@app_commands.describe(ingame_name="Ingame name of the member")
@app_commands.checks.has_role("Botadmin")
async def ping_again(interaction: discord.Interaction, ingame_name: str):
    await execute_ping_again(interaction, ingame_name)


@tree.command(name="addcompetition", description="Add a competitor guild")
@app_commands.describe(guild_id="ID of the competitor guild")
@app_commands.describe(guild_lable="Lable that should be used for the added guild")
@app_commands.checks.has_role("Botadmin")
async def add_competition(interaction: discord.Interaction,
                          guild_id: int,
                          guild_lable: str):
    await execute_add_competition(interaction, guild_id, guild_lable)


# @tree.command(name="stopmessage", description="Bot will not send the periodic event message anymore")
# @app_commands.checks.has_role("Botadmin")
# async def stop_event_message(interaction: discord.Interaction):
#     await execute_stop_periodic_message(interaction)


# @tree.command(name="startmessage", description="Bot will start sending the periodic event message")
# @app_commands.checks.has_role("Botadmin")
# async def start_event_message(interaction: discord.Interaction):
#     await execute_start_periodic_message(interaction)


# @tree.command(name="seteventchannel", description="Set a channel in which the event message wild be send")
# @app_commands.checks.has_role("Botadmin")
# @app_commands.describe(channel_id="ID of the channel")
# async def set_channel_id(interaction: discord.Interaction, channel_id: int):
#     await execute_set_periodic_message_channel(interaction, channel_id)


@tree.command(name="botstatus", description="Prints information about the bot's settings")
async def botstatus(interaction: discord.Interaction):
    await execute_botstatus(interaction)

# @set_channel_id.error
# @start_event_message.error
# @stop_event_message.error
@add_competition.error
@perma_ping_avoid.error
@temp_ping_avoid.error
@ping_again.error
@remove_member.error
@link_member.error
async def missing_role_error_handler(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.MissingRole):
        await interaction.response.send_message(embed=MISSING_PERMISSION_EMBED)
    else:
        traceback.print_exception(type(error), error, error.__traceback__)

# Startup routine
def main():
    # Importand startup checks
    #if storage.get_bot_token() == "" or storage.get_periodic_channel_id == None or storage.get_guild_id() == None or storage.get_guild_lable == "":
    #    logger.critical("Important settings are missing! Please look at the config file again.")
    #    return
    
    #if storage.is_send_periodic_message():
    #    # TODO start periodic message 
    #    pass
    
    # Starting the bot
    client.run(storage.get_bot_token())


# Main
if __name__ == "__main__":
    main()
