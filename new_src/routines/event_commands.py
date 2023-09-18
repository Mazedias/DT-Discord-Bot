import discord


async def execute_summary(interaction: discord.Interaction):
    # TODO
    await interaction.response.send_message(content="Test worked")


async def execute_overview(interaction: discord.Interaction):
    # TODO 
    pass


async def execute_eventdata(interaction: discord.Interaction):
    # TODO 
    pass


async def execute_new_event(interaction: discord.Interaction,
                   event_round: str,
                   item1: str, amount1: str,
                   item2: str, amount2: str,
                   item3: str, amount3: str,
                   item4: str, amount4: str):
    # TODO
    pass


async def execute_save_event(interaction: discord.Interaction):
    # TODO
    pass


async def execute_iteminfo(interaction: discord.Interaction):
    # TODO
    pass