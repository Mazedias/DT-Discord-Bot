import math
import json
from event_calculations import calc_round, cald_base


def store_event_results(data):
    write_file_a('util/data/event_history.txt', data)


def store_event_item_info_output(output):
    with open('util/data/output.txt', "w", encoding="utf-8") as file:
        file.write(output)


def store_new_event(data: dict, event_round: int):
    base_data = {}
    if event_round != 1:
        for x in list(data.keys()):
            base_data[x] = cald_base(event_round, data[x])
    else:
        base_data = data

    # data: {item: amount}
    event = {1: base_data}
    items = list(base_data.keys())
    print(items)
    for x in range(2, 50):
        event[x] = {
            items[0]: calc_round(x, base_data[items[0]]),
            items[1]: calc_round(x, base_data[items[1]]),
            items[2]: calc_round(x, base_data[items[2]]),
            items[3]: calc_round(x, base_data[items[3]]),
        }

    write_file_a('util/data/event_data.txt', event)


def get_event_data():
    return read_last_line('util/data/event_data.txt')


def get_active_players(data):
    active_player = 0
    for x in data["players"]["data"]:
        if int(x[13]) != 0:
            active_player += 1
    return active_player


def get_don_mean(data):
    mean = 0
    counter = 0
    for x in data["players"]["data"]:
        if int(x[13]) == 0:
            continue
        mean += int(x[13])
        counter += 1
    if counter == 0:
        return 0
    return math.floor(mean / counter)


def get_overall_don(data):
    donations = 0
    for x in data["players"]["data"]:
        donations += int(x[13])
    return donations


def get_don_list(data):
    donations = []
    for x in data["players"]["data"]:
        donations.append(x[13])
    return sorted(donations)


def write_file_a(path, data: dict):
    with open(path, 'a') as file:
        file.write(f"{json.dumps(data)}\n")


def read_last_line(path) -> dict:
    with open(path, 'r') as file:
        last_line = file.readlines()[-1]
        return json.loads(last_line)