import discord
from discord import app_commands
from command_embeds import guildeventdata_create_embed, eventdata_create_embed, save_event, event_item_info
from util.config import get_dc_token
from util.data_transformation import store_new_event


TOKEN = get_dc_token()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("Bot is up and running")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@tree.command(name="eventdata", description="Zeigt Informationen zum letzten/aktuellen Event mehrerer Gilden")
async def eventdata(interaction: discord.Interaction):
    embed = eventdata_create_embed()
    with open('compdondistibution.png', "rb") as fh:
        f = discord.File(fh, filename="compdondistibution.png")
    await interaction.response.send_message(embed=embed, file=f)


@tree.command(name="guildeventdata", description="Zeigt Informationen zum letzen/aktuellen Event unserer Gilde")
async def guildeventdata(interaction: discord.Interaction):
    embed = guildeventdata_create_embed()
    with open('dondistribution.png', "rb") as fh:
        f = discord.File(fh, filename="dondistribution.png")
    await interaction.response.send_message(embed=embed, file=f)


@tree.command(name="newevent", description="Trage ein neues Event ein.")
@app_commands.describe(event_round="Runde")
@app_commands.describe(item1="Item 1")
@app_commands.describe(amount1="Startanzahl Item 1")
@app_commands.describe(item2="Item 2")
@app_commands.describe(amount2="Startanzahl Item 2")
@app_commands.describe(item3="Item 3")
@app_commands.describe(amount3="Startanzahl Item 3")
@app_commands.describe(item4="Item 4")
@app_commands.describe(amount4="Startanzahl Item 4")
async def newevent(interaction: discord.Interaction,
                   event_round: str,
                   item1: str, amount1: str,
                   item2: str, amount2: str,
                   item3: str, amount3: str,
                   item4: str, amount4: str):
    store_new_event({item1: amount1, item2: amount2, item3: amount3, item4: amount4}, int(event_round))
    await interaction.response.send_message("Ok.")


@tree.command(name="saveevent", description="!!ADMINS ONLY!! Speichert die Daten zum letzten Event.")
async def saveevent(interaction: discord.Interaction):
    embed = save_event()
    await interaction.response.send_message(embed=embed)


@tree.command(name="eventiteminfo", description="Zeigt Informationen über die Event Stufen")
async def eventiteminfo(interaction: discord.Interaction):
    output = event_item_info()
    with open('util/data/output.txt', "rb") as file:
        await interaction.response.send_message(file=discord.File(file, "output.txt"))


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()
