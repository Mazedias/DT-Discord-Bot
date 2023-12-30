"""
Contains methods to process player or event data
"""
import math
from storage.data_api import get_total_donations, get_active_players
from storage.storage_api import get_item_reciep, get_item, get_active_event, change_event
from game.dataclasses import Item, Event, Guild


def get_donation_mean(guild_id: int) -> int:
    """
    Calculates the the donation mean of the last/current event.
    :param guild_id: ID of the guild
    :return: Donation mean
    """
    return math.floor(get_total_donations(guild_id) / get_active_players(guild_id))


def calc_round(event_round: int, base: int) -> int:
    """
    Calculates the amount of items needed for a specific round
    :param event_round: Round
    :param base: Base amount of the item
    :return: Amount of items needed to complete the round
    """
    return math.floor(int(base) * 0.9202166811 * math.exp(event_round / 8))


def calc_item_info(event: Event, limit: int) -> dict:
    """
    Calculates item data for each round <= limit with calc_round and returns
    a dictionary
    :param event: Active event
    :param limit: Round up to which the calculation is made
    :return: Dictionary with round data
    """
    rounds = {}

    rounds.update(
        {1: {event.first_item.name : event.first_item_base_amount,
             event.second_item.name : event.second_item_base_amount,
             event.third_item.name : event.third_item_base_amount,
             event.fourth_item.name : event.fourth_item_base_amount}
    })

    for i in range(2, limit+1):
        rounds.update(
            {i: {
                event.first_item.name : calc_round(i, event.first_item_base_amount),
                event.second_item.name : calc_round(i, event.second_item_base_amount),
                event.third_item.name : calc_round(i, event.third_item_base_amount),
                event.fourth_item.name : calc_round(i, event.fourth_item_base_amount),
            }}
        )

    return rounds


def cald_base(event_round: int, amount: int) -> int:
    """
    Calculates the base amount for an item
    :param event_round: Round
    :param amount: Items needed to complete the next round
    :return: Base amount of items
    """
    return math.ceil(int(amount) / (0.9202166811 * math.exp(int(event_round) / 8)))


def get_item_point_value(item: Item, amount: int) -> int:
    """
    Calcualtes the point value of a number of items
    :param item: Item
    :param amount: Amount of the item
    :return: Point value of the items
    """
    return math.floor((item.price * amount)/1000)


def predict_current_round(points: int, event: Event) -> int:
    """
    Calculates the current round based on the donation points and the point value of
    the items at the current/last event
    :param points: Donations points of a guild
    :param event: Event based on which the rounds shall be calculated
    :return: Current round
    """
    round = 0
    while(True):
        needed_points = 0

        if round == 0:
            needed_points += get_item_point_value(event.first_item, event.first_item_base_amount) + \
                get_item_point_value(event.second_item, event.second_item_base_amount) + \
                get_item_point_value(event.third_item, event.third_item_base_amount) + \
                get_item_point_value(event.fourth_item, event.fourth_item_base_amount)
        else:
            needed_points += get_item_point_value(event.first_item, calc_round(round+1, event.first_item_base_amount)) + \
                get_item_point_value(event.second_item, calc_round(round+1, event.second_item_base_amount)) + \
                get_item_point_value(event.third_item, calc_round(round+1, event.third_item_base_amount)) + \
                get_item_point_value(event.fourth_item, calc_round(round+1, event.fourth_item_base_amount))
        
        if needed_points <= points:
            round += 1
            points -= needed_points
        else:
            return round


def get_mul_production_time(items: dict[str, int]) -> int:
    """
    Calculates the time in hours needed to produce multiple items with max buildings by one player without boosts
    and without regarding that multiple items could be produced in the same building
    :param items: Dictionary containing items {item: amount}
    :return: Production time in hours
    """
    total_time = 0
    
    for item in items:
        total_time += get_production_time(get_item(item), items.get(item))

    return total_time


def get_production_time(item: Item, amount: int) -> int:
    """
    Calculates the time in hours needed to produce the given amount of the given item by one player without
    boosts on 8 slots
    :param item: The item that shall be produces
    :param amount: Amount of the item
    :return: Prodcution time in hours (may be 0)
    """
    if item.raw_item:
        return 0
    
    needed_resources = _find_subrecieps(item)
    production_time = get_item_reciep(item).time * amount

    for resource in needed_resources:
        if get_item(resource).raw_item:
            continue
        needed_resources[resource] *= amount
        production_time += get_item_reciep(get_item(resource)).time * needed_resources.get(resource)

    return math.floor((production_time) / 60 / 60 / 8)


def update_active_event(competition: list[Guild], guild: Guild, deactivate: bool):
    active_event = get_active_event()

    competition_info = {}
    for comp in competition:
        competition_info.update(
            {comp.lable: [predict_current_round(get_total_donations(comp.id), active_event), get_total_donations(comp.id), get_active_players(comp.id)]}
        )

    active_event.overall_donations = get_total_donations(guild.id)
    active_event.reached_round = predict_current_round(active_event.overall_donations, active_event)
    active_event.active_players = get_active_players(guild.id)
    active_event.competition = competition_info

    change_event(active_event, deactivate)


def _find_subrecieps(item: Item) -> dict[str : int]:
    items = {}


    for reciep in get_item_reciep(item).resources:

        if get_item(reciep).raw_item:
            continue

        items.update({reciep : get_item_reciep(item).resources.get(reciep)})
        items = _merge_reciep_dicts(items, _find_subrecieps(get_item(reciep)))

    return items

def _merge_reciep_dicts(a: dict[str : int], b: dict[str : int]) -> dict:
    for element in b:
        if element in a: 
            a[element] += b[element]
        else:
            a.update({element : b[element]})
    
    return a