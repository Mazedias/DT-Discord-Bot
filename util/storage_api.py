"""
Interface to the storage files
"""
import json
import os
from util.calculations import cald_base, calc_round
from util.data_api import get_guild_name, http_req


def get_event_data() -> dict:
    """
    Reads the lasted stored event data and returns it
    :return: Event data in dictionary
    """
    return __read_last_line('util/data/event_data.txt')


def store_new_event(event_round, item1, amount_item1, item2, amount_item2, item3, amount_item3, item4, amount_item4):
    """
    Stores new event data
    :param event_round: Round that is to complete next (f.e. : 1 if base data is passed)
    :param item1: Name of first item
    :param amount_item1: Needed amount of first item to complete next round
    :param item2: Name of second item
    :param amount_item2: Needed amount of second item to complete next round
    :param item3: Name of third item
    :param amount_item3: Needed amount of third item to complete next round
    :param item4: Name of fourth
    :param amount_item4: Needed amount of fourth item to complete next round
    :return: None
    """
    base_data = {}

    # Check if base data is already passed
    if int(event_round) != 1:
        base_data[item1] = cald_base(event_round, int(amount_item1))
        base_data[item2] = cald_base(event_round, int(amount_item2))
        base_data[item3] = cald_base(event_round, int(amount_item3))
        base_data[item4] = cald_base(event_round, int(amount_item4))
    else:
        base_data = {
            item1: int(amount_item1),
            item2: int(amount_item2),
            item3: int(amount_item3),
            item4: int(amount_item4)
        }

    # Calculate each round until round 50
    event = {1: base_data}
    items = list(base_data.keys())
    for x in range(2, 65):
        event[x] = {
            items[0]: calc_round(x, base_data[items[0]]),
            items[1]: calc_round(x, base_data[items[1]]),
            items[2]: calc_round(x, base_data[items[2]]),
            items[3]: calc_round(x, base_data[items[3]]),
        }

    # Store calculation results
    __append_dict_to_file('util/data/event_data.txt', event)


def store_event_results(guild_ids: list):
    """
    Stores event results
    :return: None
    """
    event_data = {}

    for guild_id in guild_ids:
        event_data[get_guild_name(guild_id)] = http_req(guild_id)

    __append_dict_to_file('util/data/event_history.txt', event_data)


def store_event_item(data):
    """
    Stores data in 'output.txt'. Used to store information about the needed resources for each round in the event
    :param data:
    :return:
    """
    __overwrite_file('util/data/output.txt', data)


def __overwrite_file(path, data):
    """
    Overrides a file
    :param path: Path to file
    :param data: Data to write
    :return: None
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(data)


def __append_dict_to_file(path, data: dict):
    """
    Write a dictionary to the end of a file
    :param path: Path to file
    :param data: Data to write
    :return: None
    """
    with open(path, "a") as file:
        file.write(f"{json.dumps(data)}\n")


def __read_last_line(path) -> dict:
    """
    Reads a file and returns the last line as dictionary
    :param path: Path to file
    :return: Last line of the file as a dictionary
    """
    with open(path, "r") as file:
        return json.loads(file.readlines()[-1])


def __clear_file(path) -> bool:
    """
    Clear a file
    :param path: Path to file
    :return: True if file was cleared
    """
    if not os.path.isfile(path):
        return False

    with open(path, "w") as file:
        return True


def __delete_file(path) -> bool:
    """
    Delets a file
    :param path: Path to file
    :return: True if files was deleted
    """
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False
