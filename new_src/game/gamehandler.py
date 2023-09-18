from new_src.game.dataclasses import Guild
from new_src.storage.storage_api import load_competition


class Gamehandler():
    guilds: list[Guild]

    def __init__(self) -> None:
        self.guilds = load_competition()

    def add_guild(self, guild: Guild):
        self.guilds.append(guild)