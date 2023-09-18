from src.new.util.game.game_dataclasses import Event, Item
import datetime


def add_competition(event: Event, guild_name: str, reached_round: int, active_player: int) -> Event:
    """
    This method adds information about a competitor to the event. It the competitor is already
    listed the existing information will be overridden
    :param event: Event to add the competition to
    :param guild_name: Name of the competitor guild
    :param reached_round: Reached round
    :param active_player: Active players
    :return: Returns the updated event
    """
    if (not event.active) and (guild_name not in event.competition.keys()):
        print(f"### NOTIFICATION: Competitor was added to an inactive event! "
              f"Year: {event.calendar_year} | Week: {event.calendar_week} "
              f"--- added '{guild_name}' with round {reached_round} and {active_player} active players")
    elif (not event.active) and (guild_name in event.competition.keys()):
        print(f"### NOTIFICATION: Competitor was updated to an inactive event! "
              f"Year: {event.calendar_year} | Week: {event.calendar_week} "
              f"--- updated '{guild_name}' from with round {reached_round} and {active_player} active players")

    event.competition[guild_name] = (reached_round, active_player)
    
    return event


def update_donations(event: Event, donation_amount: int) -> Event:
    """
    Method to update/change the active player of an evnet
    :param event: Event to be changed
    :param donation_amount: New overall donation amount
    :return: Returns the changed event
    """
    if not event.active:
        print(f"### NOTIFICATION: Donation amount of an inactive event was changed! "
              f"Year: {event.calendar_year} | Week: {event.calendar_week} "
              f"--- from {event.overall_donations} to {donation_amount}")

    event.overall_donations = donation_amount

    return event


def update_active_player(event: Event, active_player: int) -> Event:
    """
    Method to update/change the active player of an evnet
    :param event: Event to be changed
    :param active_player: New reached round
    :return: Returns the changed event
    """
    if not event.active:
        print(f"### NOTIFICATION: Active_player of an inactive event was changed! "
              f"Year: {event.calendar_year} | Week: {event.calendar_week} "
              f"--- from {event.active_players} to {active_player}")

    event.active_players = active_player

    return event


def update_reached_round(event: Event, new_round: int) -> Event:
    """
    Method to update/change the reached round of an evnet
    :param event: Event to be changed
    :param new_round: New reached round
    :return: Returns the changed event
    """
    if not event.active:
        print(f"### NOTIFICATION: Reached round of an inactive event was changed! "
              f"Year: {event.calendar_year} | Week: {event.calendar_week} "
              f"--- from {event.reached_round} to {new_round}")

    event.reached_round = new_round

    return event


def deactivate_event(event: Event) -> Event:
    """
    Method to mark a event as not active
    :param event: Event to deactivate
    :return: Returns the deactivated event
    """
    event.active = False

    return event


def edit_items(event: Event,
               first_item: Item, first_amount: int,
               second_item: Item, second_amount: int,
               third_item: Item, third_amount: int,
               fourth_item: Item, fourth_amount: int) -> Event:
    """
    Method to edit items of a event
    :param event: Event to be changed
    :param first_item: First Item
    :param first_amount: Needed base amount of first item
    :param second_item: Second Item
    :param second_amount: Needed base amount of second item
    :param third_item: Third Item
    :param third_amount: Needed base amount of third item
    :param fourth_item: Foruth Item
    :param fourth_amount: Needed base amount of fourth item
    :return: Returns an Event
    """
    if not event.active:
        print(f"### NOTIFICATION: Items of an inactive event were changed! "
              f"Year: {event.calendar_year} | Week: {event.calendar_week}")

    event.first_item = first_item
    event.first_item_base_amount = first_amount
    event.second_item = second_item
    event.second_item_base_amount = second_amount
    event.third_item = third_item
    event.third_item_base_amount = third_amount
    event.fourth_item = fourth_item
    event.fourth_item_base_amount = fourth_amount

    return event


def create_event(first_item: Item, first_amount: int,
                 second_item: Item, second_amount: int,
                 third_item: Item, third_amount: int,
                 fourth_item: Item, fourth_amount: int) -> Event:
    """
    Method to create a event
    :param first_item: First Item
    :param first_amount: Needed base amount of first item
    :param second_item: Second Item
    :param second_amount: Needed base amount of second item
    :param third_item: Third Item
    :param third_amount: Needed base amount of third item
    :param fourth_item: Foruth Item
    :param fourth_amount: Needed base amount of fourth item
    :return: Returns an Event
    """
    return Event(
        calendar_year=datetime.datetime.now().isocalendar()[0],
        calendar_week=datetime.datetime.now().isocalendar()[1],
        reached_round=0,
        active_players=0,
        overall_donations=0,
        active=True,
        competition={},  # TODO create method to get competition infos to store here
        first_item=first_item,
        first_item_base_amount=first_amount,
        second_item=second_item,
        second_item_base_amount=second_amount,
        third_item=third_item,
        third_item_base_amount=third_amount,
        fourth_item=fourth_item,
        fourth_item_base_amount=fourth_amount
    )
