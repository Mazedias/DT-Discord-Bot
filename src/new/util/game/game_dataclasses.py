from dataclasses import dataclass


@dataclass
class Item:
    """
    Dataclass to represent an ingame item
    """
    name: str
    price: int
    raw_item: bool  # Craftable


@dataclass
class Reciep:
    """
    Dataclass to represent an ingame crafting recept
    """
    item: Item
    time: int
    amount: int
    resources: list[(int, Item)]  # (amount, Item)


@dataclass
class Player:
    """
    Dataclass to represent a player
    """
    ingame_name: str
    last_event_donation: int
    donation_ranking: int
    discord_id: str


@dataclass
class Event:
    """
    Dataclass to represent an ingame guild event
    """
    calendar_year: int
    calendar_week: int
    reached_round: int
    active_players: int
    overall_donations: int
    active: bool
    competition: dict[str, (int, int)]
    first_item: Item
    first_item_base_amount: int
    second_item: Item
    second_item_base_amount: int
    third_item: Item
    third_item_base_amount: int
    fourth_item: Item
    fourth_item_base_amount: int
