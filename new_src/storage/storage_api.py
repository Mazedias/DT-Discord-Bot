import yaml
import storage.logging_config as logging
from game.dataclasses import Guild


CONFIG_PATH = "new_src/storage/files/config.yaml"

logger = logging.logger


def add_competition(guild: Guild):
    config = _get_config()["gamedata"]["competition"]
    guild_info = {guild.id: guild.lable}

    config.append(guild_info)

    with open(CONFIG_PATH, "w") as config_file:
        yaml.dump(config, config_file, default_flow_style=False)


def load_competition() -> list[Guild]:
    config = _get_config()["gamedata"]["competition"]
    guilds = []

    for guild in config:
        id = guild.keys()[0]
        lable = guild.get(id)
        guilds.append(Guild(id, lable))

    return guilds


def get_bot_token() -> str:
    return _get_config()["startup"]["bot_token"]


def get_periodic_channel_id() -> int:
    return _get_config()["startup"]["periodic_channel_id"]


def is_send_periodic_message() -> bool:
    return _get_config()["bot_setup"]["send_periodic_message_during_events"]


def get_periodic_time_frame() -> int:
    return _get_config()["bot_setup"]["periodic_time_frame"]


def get_guild_id() -> int:
    return _get_config()["gamedata"]["guild"]["id"]


def get_guild_lable() -> str:
    return _get_config()["gamedata"]["guild"]["lable"]


def _get_config():
    with open(CONFIG_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config
