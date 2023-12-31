import discord
import pandas as pd
import numpy as np
import dataframe_image as dfi
from matplotlib import pyplot as plt

import storage.logging_config as logger
from game.calculations import get_total_donations, get_mul_production_time, predict_current_round, calc_item_info, cald_base, update_active_event, get_active_players, get_donation_mean
from storage.storage_api import get_active_event, add_event, load_competition, get_guild, load_players, add_player, remove_player
from storage.data_api import get_donations, get_inactive_players
from routines.utils import IN_PROCESS_EMBED, UNDER_CONSTRUCTION_EMBED
from routines.utils import get_detailed_error_embed, get_simple_message_embed, get_success_message, get_detailed_embed

logger = logger.logger


async def execute_summary(interaction: discord.Interaction):
    logger.info(f"'execute_summary' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    try:
        event = get_active_event()
    except LookupError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed("No active event was found"))
        logger.error(f"'execute_summary' failed with error: LookupError since no active event was found")
        return

    guild = get_guild()
    opponents = load_competition()

    if len(opponents) == 0:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed("No guilds to track configured! Add some with '/addcompetition'."))
        logger.error(f"'execute_summary' failed because no guilds to track where conigured.")
        return

    # Create summary output text for the embed
    inactive_players = get_inactive_players(get_guild().id)
    info_output = f"```{guild.lable}: Runde {predict_current_round(get_total_donations(guild.id), event)}"
    for opponent in opponents:
        info_output = f"{info_output}\n{opponent.lable}: Runde {predict_current_round(get_total_donations(opponent.id), event)}"
    
    info_output = f"{info_output}```"
    info_output = f"{info_output}```Inactive Players:"

    for p in load_players():
        if (p.ingame_name in inactive_players) and (p.temp_ping and p.perma_ping):
            info_output = f"{info_output}\n{p.discord_id}"
            inactive_players.remove(p.ingame_name)
    
    info_output = f"{info_output}\n\nUnlinked Inactive Players:"

    for p in inactive_players:
        info_output = f"{info_output}\n{p}"

    info_output = f"{info_output}```"
    
    message_embed = get_simple_message_embed("Event Summary", info_output)

    await interaction.edit_original_response(content=None, embed=message_embed)


async def execute_overview(interaction: discord.Interaction):
    logger.info(f"'execute_summary' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=UNDER_CONSTRUCTION_EMBED)


async def execute_eventdata(interaction: discord.Interaction):
    logger.info(f"'execute_eventdata' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    guild = get_guild()
    competition = load_competition()

    try:
        get_active_event()
    except LookupError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed("No active event was found"))
        logger.error(f"'execute_eventdata' failed with error: LookupError since no active event was found")
        return

    # Generate Plot
    plt.title("Player Donation Distribution")
    plt.plot(np.array(get_donations(guild.id)), "green", label=guild.lable, linestyle="dotted")

    # Generate embed fields
    fields = []
    fields.append(
        (
            f"Eventinformationen zu {guild.lable}",
            f"• Aktive Spieler: {get_active_players(guild.id)}\n• Durchschnittliche Spenden: {get_donation_mean(guild.id)}\n• Insgesamte Spenden: {get_total_donations(guild.id)}\n• Geschätze Runde: {predict_current_round(get_total_donations(guild.id), get_active_event())}"
        )
    )

    for comp in competition:
        # Gather data
        active = get_active_players(comp.id)
        total_donations = get_total_donations(comp.id)
        donation_mean = get_donation_mean(comp.id)
        round = predict_current_round(total_donations, get_active_event())
        

        plt.plot(np.array(get_donations(comp.id)), label=comp.lable, linestyle="solid")
        fields.append(
            (
                f"Eventinformationen zu {comp.lable}",
                f"• Aktive Spieler: {active}\n• Durchschnittliche Spenden: {donation_mean}\n• Insgesamte Spenden: {total_donations}\n• Geschätze Runde: {round}"
            )
        )
    
    plt.legend()
    plt.savefig("./src/storage/files/compDonDistribution.png", bbox_inches="tight")
    plt.close()
    
    embed = get_detailed_embed(
        title="Player donation distribution",
        description="Informationen über die verteilung der Spenden über die einzelne Spieler.",
        fields=fields
    )
    embed.set_image(url="attachment://compDonDistribution.png")

    with open('./src/storage/files/compDonDistribution.png', "rb") as fh:
        f = discord.File(fh, filename="compDonDistribution.png")

    await interaction.edit_original_response(content=None, embed=embed, attachments=[f])


async def execute_new_event(interaction: discord.Interaction,
                   event_round: str,
                   item1: str, amount1: str,
                   item2: str, amount2: str,
                   item3: str, amount3: str,
                   item4: str, amount4: str):
    logger.info(f"'execute_new_event' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)
    
    try:
        add_event(
            event_round, 
            item1, cald_base(int(event_round), int(amount1)), 
            item2, cald_base(int(event_round), int(amount2)), 
            item3, cald_base(int(event_round), int(amount3)), 
            item4, cald_base(int(event_round), int(amount4))
        )
        
    except (NameError, LookupError) as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(f"Error: {e}"))
        logger.error(f"'execute_new_event' failed with error: {e}")
        return
    
    await interaction.edit_original_response(content=None, embed=get_success_message())


async def execute_save_event(interaction: discord.Interaction):
    logger.info(f"'execute_save_event' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)

    try:
        update_active_event(load_competition(), get_guild(), True)
    except LookupError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(
            "No active Event was found!"
        ))
        logger.error(f"'execute_save_event' failed with error {e}")
        return

    # Activate Temp ping for everyone again
    players = load_players()
    for p in players:
        p.temp_ping = True
        try:
            remove_player(p.ingame_name)
            add_player(p)
        except KeyError as e:
            continue


    await interaction.edit_original_response(content=None, embed=get_success_message())
    

async def execute_iteminfo(interaction: discord.Interaction, start: int, limit: int):
    logger.info(f"'execute_iteminfo' called by Name:{interaction.user.name} | ID:{interaction.user.id} from Server:{interaction.guild.name} | ID:{interaction.guild.id}")
    await interaction.response.send_message(embed=IN_PROCESS_EMBED)
    
    try:
        event = get_active_event()
    except LookupError as e:
        await interaction.edit_original_response(content=None, embed=get_detailed_error_embed(f"Error: {e}"))
        logger.error(f"'execute_iteminfo' failed with error: {e}")
        return
    
    round_data = calc_item_info(event, limit)

    data = {
        "Round":[],
        f"{event.first_item.name}": [],
        f"{event.second_item.name}": [],
        f"{event.third_item.name}": [],
        f"{event.fourth_item.name}": [],
        #"Production Time": []
    }

    for round in round_data:
        data.get("Round").append(round)
        data.get(event.first_item.name).append(round_data.get(round).get(event.first_item.name))
        data.get(event.second_item.name).append(round_data.get(round).get(event.second_item.name))
        data.get(event.third_item.name).append(round_data.get(round).get(event.third_item.name))
        data.get(event.fourth_item.name).append(round_data.get(round).get(event.fourth_item.name))
        #data.get("Production Time").append(get_mul_production_time({
        #    event.first_item.name : round_data.get(round).get(event.first_item.name),
        #    event.second_item.name : round_data.get(round).get(event.second_item.name),
        #    event.third_item.name : round_data.get(round).get(event.third_item.name),
        #    event.fourth_item.name : round_data.get(round).get(event.fourth_item.name),
        #})) # TODO too fucking slow right now :(
    
    data.get("Round").append("Sum")
    data.get(event.first_item.name).append(np.sum(data.get(event.first_item.name)))
    data.get(event.second_item.name).append(np.sum(data.get(event.second_item.name)))
    data.get(event.third_item.name).append(np.sum(data.get(event.third_item.name)))
    data.get(event.fourth_item.name).append(np.sum(data.get(event.fourth_item.name)))
    
    
    df = pd.DataFrame(data=data).set_index("Round")
    df = df.iloc[(start-1):]
    
    df_styled = df.style.background_gradient()
    dfi.export(df_styled, './src/storage/files/df_styled.png', table_conversion="matplotlib")

    df.to_csv(path_or_buf='./src/storage/files/iteminfo.csv')

    await interaction.edit_original_response(embed=None, attachments=[discord.File('./src/storage/files/df_styled.png'), discord.File('./src/storage/files/iteminfo.csv')])

