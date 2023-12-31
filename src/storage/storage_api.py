import yaml
import datetime
import storage.logging_config as logger
from game.dataclasses import Guild, Player, Event, Item, Reciep


CONFIG_PATH = "./src/storage/files/config.yaml"
ITEMS_PATH = "./src/storage/files/items.yaml"

logger = logger.logger


def add_competition(guild: Guild):
    config = _get_config()
    guild_info = {guild.id: guild.lable}

    config["gamedata"]["competition"].update(guild_info)

    _write_config(config)


def load_competition() -> list[Guild]:
    config = _get_config()["gamedata"]["competition"]
    guilds = []

    for guild in config:
        guilds.append(Guild(guild, config.get(guild)))

    return guilds


def add_player(player: Player):
    config = _get_config()
    player_info = {player.ingame_name: [player.discord_id, player.temp_ping, player.perma_ping]}

    for p in config["gamedata"]["players"]:
        if player.ingame_name in p.keys():
            raise KeyError()

    config["gamedata"]["players"].append(player_info)

    _write_config(config)


def remove_player(playername: str):
    config = _get_config()

    found = False

    for p in config["gamedata"]["players"]:
        if playername in p.keys():
            config["gamedata"]["players"].remove(p)
            found = True
        
    if not found:
        raise KeyError

    _write_config(config)


def load_players() -> list[Player]:
    config = _get_config()["gamedata"]["players"]
    players = []

    for player in config:
        name = list(player.keys())[0]
        tag = player.get(name)[0]
        temp_ping = player.get(name)[1]
        perma_ping = player.get(name)[2]
        players.append(Player(name, tag, temp_ping, perma_ping))
    
    return players


def add_event(event_round,
                item1: str, amount1: int,
                item2: str, amount2: int,
                item3: str, amount3: int,
                item4: str, amount4: int):
    
    first_item = get_item(item1)
    second_item = get_item(item2)
    third_item = get_item(item3)
    fourth_item = get_item(item4)
    year = datetime.datetime.now().isocalendar()[0]
    week = datetime.datetime.now().isocalendar()[1]

    config = _get_config()
    event_info = {
        "round":0,
        "players":0,
        "donations":0,
        "active":True,
        "competition":{},
        "item1":[first_item.name, first_item.price, first_item.raw_item],
        "a_item1":amount1,
        "item2":[second_item.name, second_item.price, second_item.raw_item],
        "a_item2":amount2,
        "item3":[third_item.name, third_item.price, third_item.raw_item],
        "a_item3":amount3,
        "item4":[fourth_item.name, fourth_item.price, fourth_item.raw_item],
        "a_item4":amount4,
    }

    if year in config["gamedata"]["events"]:
        if week in config["gamedata"]["events"][year]:
            raise LookupError("Already exists")
        else:
            config["gamedata"]["events"][year].update({
                week: event_info
            })
    else:
        config["gamedata"]["events"].update({year: {
                week: event_info
        }})
    
    _write_config(config)


def load_events() -> list[Event]:
    config = _get_config()["gamedata"]["events"]
    events = []

    for year in config:
        for week in config[year]:
            data = config[year][week]
            event = Event(
                calendar_year=year,
                calendar_week=week,
                reached_round=data.get('round'),
                active_players=data.get('players'),
                overall_donations=data.get('donations'),
                active=data.get('active'),
                competition=data.get('competition'),
                first_item=Item(
                    data.get('item1')[0],
                    data.get('item1')[1],
                    data.get('item1')[2]
                ),
                first_item_base_amount=data.get('a_item1'),
                second_item=Item(
                    data.get('item2')[0],
                    data.get('item2')[1],
                    data.get('item2')[2]
                ),
                second_item_base_amount=data.get('a_item2'),
                third_item=Item(
                    data.get('item3')[0],
                    data.get('item3')[1],
                    data.get('item3')[2]
                ),
                third_item_base_amount=data.get('a_item3'),
                fourth_item=Item(
                    data.get('item4')[0],
                    data.get('item4')[1],
                    data.get('item4')[2]
                ),
                fourth_item_base_amount=data.get('a_item4')
            )

            events.append(event)
    
    return events


def get_active_event() -> Event:
    events = load_events()

    active_events = []

    for event in events:
        if event.active:
            active_events.append(event)

    if len(active_events) > 1:
        raise LookupError("Multiple active events found!")
    elif len(active_events) == 0:
        raise LookupError("No active event found!")

    return active_events[0]


def change_event(event: Event, change_active: bool):
    config = _get_config()

    if event.calendar_year not in config["gamedata"]["events"] or event.calendar_week not in config["gamedata"]["events"][event.calendar_year]:
        raise LookupError("Can't change non existing event! Please add it first.")

    new_event_info = {
        "round":event.reached_round,
        "players":event.active_players,
        "donations":event.overall_donations,
        "active": not change_active,
        "competition":event.competition,
        "item1":[event.first_item.name, event.first_item.price, event.first_item.raw_item],
        "a_item1":event.first_item_base_amount,
        "item2":[event.second_item.name, event.second_item.price, event.second_item.raw_item],
        "a_item2":event.second_item_base_amount,
        "item3":[event.third_item.name, event.third_item.price, event.third_item.raw_item],
        "a_item3":event.third_item_base_amount,
        "item4":[event.fourth_item.name, event.fourth_item.price, event.fourth_item.raw_item],
        "a_item4":event.fourth_item_base_amount,
    }

    config["gamedata"]["events"][event.calendar_year].update(
        {event.calendar_week: new_event_info}
    )

    _write_config(config)


def get_item(name: str) -> Item:
    items = _get_items()["items"]

    if name in items:
        data = items[name]
        return Item(name, data.get("price"), data.get("raw"))
    else:
        raise NameError(f"The Item '{name}' is unknown to me!")


def get_item_reciep(item: Item) -> Reciep:
    recieps = _get_items()["recieps"]

    if item.name in recieps:
        return Reciep(item,recieps[item.name]["time"],recieps[item.name]["amount"],recieps[item.name]["resources"])
    else:
        raise NameError()
    

def get_bot_token() -> str:
    return _get_config()["startup"]["bot_token"]


def get_periodic_channel_id() -> int:
    return _get_config()["startup"]["periodic_channel_id"]


def is_send_periodic_message() -> bool:
    return _get_config()["bot_setup"]["send_periodic_message_during_events"]


def get_periodic_time_frame() -> int:
    return _get_config()["bot_setup"]["periodic_time_frame"]


def get_guild() -> Guild:
    config = _get_config()["gamedata"]["guild"]

    return Guild(config["id"], config["label"])


def _get_items():
    with open(ITEMS_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def _get_config():
    with open(CONFIG_PATH, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def _write_config(config):
    with open(CONFIG_PATH, "w") as config_file:
        yaml.dump(config, config_file, default_flow_style=False)
