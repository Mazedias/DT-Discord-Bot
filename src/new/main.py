import discord
from discord import app_commands
import asyncio


TOKEN = "MTExNzA3MDIxMzkwNTY0OTcxNw.G1ghhu.pmA_1l4cUZrag2s6Xc8nK_U4vkf3mHnWu-lWlE"
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
CHANNEL_ID = 1117071205745295481


@tree.command(name="test_command")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("Test Command was executed")


@tree.command(name="start_message")
async def start_periodic_message(interaction: discord.Interaction):
    await interaction.response.send_message("Starting periodic message")
    client.loop.create_task(send_periodic_message())


@tree.command(name="stop_message")
async def stop_periodic_message(interaction: discord.Interaction):
    pass


async def send_periodic_message():
    await client.wait_until_ready()

    while not client.is_closed():
        channel = client.get_channel(CHANNEL_ID)
        await channel.send("Periodic test message!")

        await asyncio.sleep(15)


@client.event
async def on_ready():
    print("Bot is up and running")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    # Start periodic routines
    asyncio.create_task(send_periodic_message())


if __name__ == "__main__":
    client.run(TOKEN)
