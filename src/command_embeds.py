import datetime

import discord
import numpy as np
from matplotlib import pyplot as plt
from table2ascii import table2ascii as t2a, PresetStyle

from util.calculations import get_mul_production_time, get_donation_mean, get_total_donations, predict_current_round
from util.data_api import get_donations, get_active_players
from util.storage_api import get_event_data, store_event_item, store_event_results, get_event_review_activeplayerlist, \
    get_event_review_eventrounds


def create_summary():
    g_id = 75
    d_id = 1
    p_id = 271
    message = f"Aktueller Stand: \n```" \
              f"-> Wir: Runde {predict_current_round(get_total_donations(g_id), get_event_data())}\n" \
              f"-> Permonici: Runde {predict_current_round(get_total_donations(p_id), get_event_data())}\n" \
              f"-> Deep and Dirty: Runde {predict_current_round(get_total_donations(d_id), get_event_data())}```"
    return message


def create_overview():
    # Create plots
    # Active player plot
    activeplayerlist_dad = np.array(get_event_review_activeplayerlist(1))
    activeplayerlist_gmc = np.array(get_event_review_activeplayerlist(75))
    activeplayerlist_pcz = np.array(get_event_review_activeplayerlist(271))

    plt.title("Event active player history")
    plt.plot(activeplayerlist_dad, "blue", label="GMC", linestyle="-")
    plt.plot(activeplayerlist_gmc, "green", label="DAD", linestyle="-.")
    plt.plot(activeplayerlist_pcz, "red", label="PCZ", linestyle=":")
    plt.legend()
    plt.savefig('eventactiveplayer.png', bbox_inches='tight')
    plt.close()

    # Reached round plot
    eventrounds_dad = np.array(get_event_review_eventrounds(1))
    eventrounds_gmc = np.array(get_event_review_eventrounds(75))
    eventrounds_pcz = np.array(get_event_review_eventrounds(271))

    plt.title("Event reached round history")
    plt.plot(eventrounds_dad, "blue", label="GMC", linestyle="-")
    plt.plot(eventrounds_gmc, "green", label="DAD", linestyle="-.")
    plt.plot(eventrounds_pcz, "red", label="PCZ", linestyle=":")
    plt.legend()
    plt.savefig('eventrounds.png', bbox_inches='tight')
    plt.close()


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
                f"{get_mul_production_time({items[0]: data.get(r).get(items[0]), items[1]: data.get(r).get(items[1]), items[2]: data.get(r).get(items[2]),items[3]: data.get(r).get(items[3]),})}"
            ]
        )

    output = t2a(
            header=["Runde", f"{items[0]}", f"{items[1]}", f"{items[2]}", f"{items[3]}", "Zeit (h)"],
            body=event_rounds,
            style=PresetStyle.thin_compact
    )
    store_event_item(output)
    return output


def save_event() -> discord.Embed:
    dates = ["Thursday", "Friday", "Saturday", "Sunday"]
    if datetime.datetime.now().strftime("%A") in dates:
        embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
        embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Fehler", value="Wärend einem Laufendem Event kann nicht gespeichert werden!")
        return embed

    store_event_results([1, 75, 271])

    embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
    embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="Done", value="Die Ergebnisse des letzten Events wurden gespeichert")
    return embed


def guildeventdata_create_embed() -> discord.Embed:
    # Guild id
    g_id = 75

    # Generate plot
    ypoints = np.array(get_donations(g_id))
    plt.plot(ypoints, "o")
    plt.savefig('dondistribution.png', bbox_inches='tight')
    plt.close()

    # Create Embedding
    embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
    embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="Evenetinformationen zu unserer Gilde",
                    value=f"• Aktive Spieler: {get_active_players(g_id)}\n"
                          f"• Durchschnittliche Spenden: {get_donation_mean(g_id)}\n"
                          f"• Insgesamte Spenden: {get_total_donations(g_id)}\n"
                          f"• Geschätze Runde: {predict_current_round(get_total_donations(g_id), get_event_data())}\n"
                          f"Spendenverteilung unter den Spielern:",
                    inline=False)
    embed.set_image(url="attachment://dondistribution.png")
    return embed


def eventdata_create_embed() -> discord.Embed:
    # Guild ids
    g_id = 75
    d_id = 1
    p_id = 271

    # Generate plot
    gmc_points = np.array(get_donations(75))  # GMC
    dad_points = np.array(get_donations(1))  # DAD
    pcz_points = np.array(get_donations(271))  # PCZ

    plt.title("Player Donation Distribution")
    plt.plot(gmc_points, "blue", label="GMC", linestyle="-")
    plt.plot(dad_points, "green", label="DAD", linestyle="-.")
    plt.plot(pcz_points, "red", label="PCZ", linestyle=":")
    plt.legend()
    plt.savefig('compdondistibution.png', bbox_inches='tight')
    plt.close()

    # Create Embedding
    embed = discord.Embed(title="Eventübersicht", colour=discord.Colour(0xbf6b0a))
    embed.set_author(name="Event Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Calculation finished...", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="Generelle Eventinformationen GMC",
                    value=f"• Aktive Spieler: {get_active_players(g_id)}\n"
                          f"• Durchschnittliche Spenden: {get_donation_mean(g_id)}\n"
                          f"• Insgesamte Spenden: {get_total_donations(g_id)}\n"
                          f"• Geschätze Runde: {predict_current_round(get_total_donations(g_id), get_event_data())}",
                    inline=False)
    embed.add_field(name="Generelle Eventinformationen DAD",
                    value=f"• Aktive Spieler: {get_active_players(d_id)}\n"
                          f"• Durchschnittliche Spenden: {get_donation_mean(d_id)}\n"
                          f"• Insgesamte Spenden: {get_total_donations(d_id)}\n"
                          f"• Geschätze Runde: {predict_current_round(get_total_donations(d_id), get_event_data())}",
                    inline=False)
    embed.add_field(name="Generelle Eventinformationen PCZ",
                    value=f"• Aktive Spieler: {get_active_players(p_id)}\n"
                          f"• Durchschnittliche Spenden: {get_donation_mean(p_id)}\n"
                          f"• Insgesamte Spenden: {get_total_donations(p_id)}\n"
                          f"• Geschätze Runde: {predict_current_round(get_total_donations(p_id), get_event_data())}",
                    inline=False)
    embed.set_image(url="attachment://compdondistibution.png")
    return embed