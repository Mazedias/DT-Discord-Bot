"""
Data connection to DTAT Web API
"""
import requests
import json


def get_players(guild_id) -> list:
    """
    Collects data with __http_req() and creates a list containing all ingame players names that are in the 
    guild with the guild_id
    """
    http_data = http_req(guild_id).get("players").get("data")
    
    playernames = []

    for player in http_data:
        playernames.append(player[1])
    
    return playernames


def get_inactive_players(guild_id) -> list:
    """
    Collects data with __http_req() and creates a list containing all ingame names of players with zero
    last event donations
    """
    http_data = http_req(guild_id).get("players").get("data")

    inactive_players = []
    for player in http_data:
        if int(player[13]) == 0:
            inactive_players.append(player[1])
        
    return inactive_players


def get_donations(guild_id) -> list:
    """
    Collects data with __http_req() and creates a sorted list of length 50 containing the amount of donations
    of each player at the current/last event
    :param guild_id: ID of the guild
    :return: List containing information about current/last event donations
    """
    http_data = http_req(guild_id).get("players").get("data")
    event_donations = []

    for player in http_data:
        event_donations.append(player[13])

    while len(event_donations) < 50:
        event_donations.append(0)

    return sorted(event_donations)


def get_total_donations(guild_id) -> int:
    """
    Collects data with __http_req() and calculates the total amount of donation points in the last/current event
    :param guild_id: ID of the guild
    :return: Total amount of donations
    """
    http_data = http_req(guild_id).get("players").get("data")
    total_donations = 0

    for player in http_data:
        total_donations += int(player[13])

    return total_donations


def get_guild_name(guild_id) -> str:
    """
    Collects data with __http_req() and returns the name of the guild assoiated with the passed guild id
    :param guild_id: ID of the guild
    :return: Guild name
    """
    return http_req(guild_id).get("name")


def get_active_players(guild_id) -> int:
    """
    Collects data with __http_req() and returns the amount of active players in the last/current event
    :param guild_id: ID of the guild
    :return: Amount of active player
    """
    http_data = http_req(guild_id).get("players").get("data")
    active_player = 0

    for player in http_data:
        if int(player[13]) != 0:
            active_player += 1

    return active_player


def get_player_amount(guild_id) -> int:
    """
    Collects data with __http_req() and returns the amount of players in the guild
    :param guild_id: ID of the guild
    :return: Amount of players
    """
    return len(http_req(guild_id).get("players").get("data"))


def http_req(guild_id):
    """
    Preforms a http request and collects data from the DTAT Web API, converts it to a dictionary
    and returns the dictionary
    :param guild_id: Id of the guild
    :return: Data as dictionary
    """
    response = requests.get(f'https://dtat.hampl.space/data/guild/id/{guild_id}/data')
    return json.loads(response.text)
