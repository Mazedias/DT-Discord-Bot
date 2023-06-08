import discord
import numpy as np
import datetime
from matplotlib import pyplot as plt
from table2ascii import table2ascii as t2a, PresetStyle
from util.dtat_bot_connection import http_req
from util.data_transformation import get_active_players, get_don_mean, get_overall_don, get_don_list, get_event_data, \
    store_event_results, store_event_item_info_output
from event_calculations import predict_cur_round, get_mul_producti_time


def event_item_info():
    data = get_event_data()
    items = list(data.get("1").keys())
    event_rounds = []
    for r in list(data.keys()):
        event_rounds.append(
            [
                f"{r}",
                f"{data.get(r).get(items[0])}",
                f"{data.get(r).get(items[1])}",
                f"{data.get(r).get(items[2])}",
                f"{data.get(r).get(items[3])}",
                f"{get_mul_producti_time({items[0]: data.get(r).get(items[0]), items[1]: data.get(r).get(items[1]), items[2]: data.get(r).get(items[2]),items[3]: data.get(r).get(items[3]),})}"
            ]
        )
    print(event_rounds)
    output = t2a(
            header=["Runde", f"{items[0]}", f"{items[1]}", f"{items[2]}", f"{items[3]}", "Zeit (h)"],
            body=event_rounds,
            style=PresetStyle.thin_compact
    )
    store_event_item_info_output(output)
    return output


def save_event() -> discord.Embed:
    dates = ["Thursday", "Friday", "Saturday", "Sunday"]
    if datetime.datetime.now().strftime("%A") in dates:
        embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
        embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Fehler", value="Wärend einem Laufendem Event kann nicht gespeichert werden!")
        return embed

    gmc_data = http_req(75)  # German Mining Company
    dad_data = http_req(1)  # Deep and Dirty
    pcz_data = http_req(271)  # Permonici CZ

    event_data = {"gmc": gmc_data, "dad": dad_data, "pcz": pcz_data}
    store_event_results(event_data)

    embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
    embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="Done", value="Die Ergebnisse des letzten Events wurden gespeichert")
    return embed


def guildeventdata_create_embed() -> discord.Embed:
    # Get http data
    data = http_req(75)

    # Generate plot
    ypoints = np.array(get_don_list(data))
    plt.plot(ypoints, "o")
    plt.savefig('dondistribution.png', bbox_inches='tight')

    # Create Embedding
    embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
    embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="Evenetinformationen zu unserer Gilde",
                    value=f"• Aktive Spieler: {get_active_players(data)}\n"
                          f"• Durchschnittliche Spenden: {get_don_mean(data)}\n"
                          f"• Insgesamte Spenden: {get_overall_don(data)}\n"
                          f"• Geschätze Runde: {predict_cur_round(get_overall_don(data), get_event_data())}\n"
                          f"Spendenverteilung unter den Spielern:",
                    inline=False)
    embed.set_image(url="attachment://dondistribution.png")
    return embed


def eventdata_create_embed() -> discord.Embed:
    gmc_data = http_req(75)  # German Mining Company
    dad_data = http_req(1)  # Deep and Dirty
    pcz_data = http_req(271)  # Permonici CZ

    # Generate plot
    gmc_points = np.array(get_don_list(gmc_data))
    while len(gmc_points) <= 50:
        gmc_points = np.insert(gmc_points, 0, 0)
    dad_points = np.array(get_don_list(dad_data))
    while len(dad_points) <= 50:
        dad_points = np.insert(dad_points, 0, 0)
    pcz_points = np.array(get_don_list(pcz_data))
    while len(pcz_points) <= 50:
        pcz_points = np.insert(pcz_points, 0, 0)

    plt.title("Player Donation Distribution")
    plt.plot(gmc_points, "blue", label="GMC", linestyle="-")
    plt.plot(dad_points, "green", label="DAD", linestyle="-.")
    plt.plot(pcz_points, "red", label="PCZ", linestyle=":")
    plt.legend()
    plt.savefig('compdondistibution.png', bbox_inches='tight')

    # Create Embedding
    embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
    embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="Generelle Eventinformationen GMC",
                    value=f"• Aktive Spieler: {get_active_players(gmc_data)}\n"
                          f"• Durchschnittliche Spenden: {get_don_mean(gmc_data)}\n"
                          f"• Insgesamte Spenden: {get_overall_don(gmc_data)}\n"
                          f"• Geschätze Runde: {predict_cur_round(get_overall_don(gmc_data), get_event_data())}",
                    inline=False)
    embed.add_field(name="Generelle Eventinformationen DAD",
                    value=f"• Aktive Spieler: {get_active_players(dad_data)}\n"
                          f"• Durchschnittliche Spenden: {get_don_mean(dad_data)}\n"
                          f"• Insgesamte Spenden: {get_overall_don(dad_data)}\n"
                          f"• Geschätze Runde: {predict_cur_round(get_overall_don(dad_data), get_event_data())}",
                    inline=False)
    embed.add_field(name="Generelle Eventinformationen PCZ",
                    value=f"• Aktive Spieler: {get_active_players(pcz_data)}\n"
                          f"• Durchschnittliche Spenden: {get_don_mean(pcz_data)}\n"
                          f"• Insgesamte Spenden: {get_overall_don(pcz_data)}\n"
                          f"• Geschätze Runde: {predict_cur_round(get_overall_don(pcz_data), get_event_data())}",
                    inline=False)
    embed.set_image(url="attachment://compdondistibution.png")
    return embed