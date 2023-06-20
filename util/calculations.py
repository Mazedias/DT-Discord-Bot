"""
Contains methods to process player or event data
"""
import math
from util.data_api import get_total_donations, get_active_players


def get_donation_mean(guild_id) -> int:
    """
    Calculates the the donation mean of the last/current event.
    :param guild_id: ID of the guild
    :return: Donation mean
    """
    return math.floor(get_total_donations(guild_id) / get_active_players(guild_id))


def calc_round(event_round, base):
    """
    Calculates the amount of items needed for a specific round
    :param event_round: Round
    :param base: Base amount of the item
    :return: Amount of items needed to complete the round
    """
    return math.floor(int(base) * 0.9202166811 * math.exp(event_round / 8))


def cald_base(event_round, amount):
    """
    Calculates the base amount for an item
    :param event_round: Round
    :param amount: Items needed to complete the next round
    :return: Base amount of items
    """
    return math.ceil(int(amount) / (0.9202166811 * math.exp(int(event_round) / 8)))


def get_item_price(item, amount):
    """
    Calcualtes the value of a number of items
    :param item: Item
    :param amount: Amount of the item
    :return: Value of the items, if item is unknown -1
    """
    if item not in deep_town_items_prices:
        return -1

    return deep_town_items_prices.get(item) * amount


def get_item_point_value(item, amount):
    """
    Calcualtes the point value of a number of items
    :param item: Item
    :param amount: Amount of the item
    :return: Point value of the items, if item is unknown -1
    """
    if item not in deep_town_items_prices:
        return -1

    return math.floor(get_item_price(item, amount)/1000)


def predict_current_round(points: int, round_data: dict):
    """
    Calculates the current round based on the donation points and the point value of
    the items at the current/last event
    :param points: Donations points of a guild
    :param round_data: Event data
    :return: Current round
    """
    round_ids = list(round_data.keys())
    round_counter = 0

    for key in round_ids:
        items = list(round_data.get(key).keys())
        needed_points = get_item_point_value(items[0], round_data.get(key).get(items[0])) + \
                        get_item_point_value(items[1], round_data.get(key).get(items[1])) + \
                        get_item_point_value(items[2], round_data.get(key).get(items[2])) + \
                        get_item_point_value(items[3], round_data.get(key).get(items[3]))
        if needed_points <= points:
            round_counter += 1
            points -= needed_points
        else:
            break

    return round_counter


def get_mul_production_time(items: dict):
    """
    Calculates the time in hours needed to produce multiple items with max buildings by one player without boosts
    and without regarding that multiple items could be produced in the same building
    :param items: Dictionary containing items {(item1, amount_item1), ...}
    :return: Production time in hours
    """
    total_time = 0

    for item in list(items.keys()):
        total_time += get_production_time(item, items.get(item))

    return total_time


def get_production_time(item, amount):
    """
    Calculates the time in hours needed to prodce the amount of items with max bildings by one player without boosts
    :param item: Item
    :param amount: Amount of item
    :return: Production time in hours, , if item is unknown -1
    """
    if item not in deep_town_item_recipes:
        return -1

    recipe = deep_town_item_recipes.get(item)
    recipe_len = len(recipe)
    production_time = round(recipe[0] / recipe[1])  # Calculate production time for 1 item
    needed_ingredients = []  # (amount, item)

    # Get all ingredients for the main item
    for x in range(2, recipe_len):
        needed_ingredients.append(recipe[x])

    # Find all subrecipes
    done = False
    while not done:
        # Find for each element in needed_ingredients the needed ingredients
        for x in range(len(needed_ingredients)):
            if needed_ingredients[x][1] in deep_town_raw_items:
                continue

            r = deep_town_item_recipes.get(needed_ingredients[x][1])
            for y in range(2, len(r)):
                if r[y] in needed_ingredients:
                    continue
                needed_ingredients.append(r[y])

        # Check if each element in needed_ingredients is either a raw item or
        # the sub recipes are already found and in needed_ingredients
        for z in range(len(needed_ingredients)):
            if needed_ingredients[z][1] not in deep_town_raw_items:
                finised = True
                p = deep_town_item_recipes.get(needed_ingredients[z][1])
                for u in range(2, len(p)):
                    if p[u] not in needed_ingredients:
                        finised = False
                        break

                if not finised:
                    break
            elif z == len(needed_ingredients) - 1:
                done = True

        return math.floor((production_time * int(amount) / 60 / 60 / 8))


# Deep Town item Data
deep_town_item_recipes = {
    # Name                      Time    Amount  Ingredient recepies
    "Amber Bracelet":           (120,   1,      (1, "Polished Amber"), (1, "Silver Bar")),
    "Copper Bar":               (10,    1,      (5, "Copper")),
    "Copper Nail":              (20,    10,     (1, "Copper Bar")),
    "Emerald Rind":             (300,   1,      (1, "Polished Emerald"), (1, "Gold Bar")),
    "Graphite":                 (5,     1,      (5, "Coal")),
    "Haircomb": (120, 1, (10, "Polished Alexandrite"), (15, "Polished Amethyst"), (1, "Silver Bar")),
    "Iron Bar": (15, 1, (5, "Iron")),
    "Maya Calendar": (120, 1, (10, "Gold Bar"), (2, "Silver Bar")),
    "Obsidian Knife": (120, 1, (50, "Polished Obsidian"), (2, "Tree"), (1, "Silver Bar")),
    "Tree": (1800, 10, (1, "Tree Seed"), (10, "Water")),
    "Wire": (30, 5, (1, "Copper Bar")),
    "Battery": (120, 1, (5, "Copper Bar"), (1, "Iron Bar"), (1, "Amber")),
    "Circuits": (180, 1, (20, "Copper Bar"), (10, "Iron Bar"), (50, "Graphite")),
    "Clean Water": (600, 1, (1, "Lab Flask"), (1, "Water")),
    "Glass": (60, 1, (2, "Silicon")),
    "Hydrogen": (900, 2, (1, "Clear Water")),
    "Lab Flask": (60, 1, (1, "Glass")),
    "Lamp": (80, 1, (20, "Graphite"), (10, "Wire"), (5, "Copper Bar")),
    "Aluminium Bottle": (30, 1, (1, "Aluminium Bar")),
    "Amber Charger": (5, 1, (1, "Amber")),
    "Amber Insulation": (20, 1, (1, "Aluminium Bottle",), (10, "Amber")),
    "Insulated Wire": (200, 1, (1, "Amber Insulation"), (1, "Wire")),
    "Aluminum Bar": (15, 1, (5, "Aluminium")),
    "Aluminum Tank": (120, 5, (3, "Aluminium Bar")),
    "Mirror": (120, 2, (1, "Silver Bar"), (1, "Glass")),
    "Mirror Laser": (120, 2, (3, "Mirror"), (1, "Lamp"), (1, "Battery")),
    "Silver Bar": (60, 1, (5, "Silver")),
    "Steel Bar": (45, 1, (1, "Graphite"), (1, "Iron Bar")),
    "Gold Bar": (60, 1, (5, "Gold")),
    "Polished Amber": (30, 1, (5, "Amber")),
    "Polished Emerald": (30, 1, (5, "Emerald")),
    "Green Laser": (20, 5, (1, "Lamp"), (1, "Insulated Wire"), (1, "Polished Emerald")),
    "Diamond Cutter": (30, 1, (5, "Polished Diamond"), (1, "Steel Plate")),
    "Ethanol": (1800, 1, (1, "Aluminium Bottle"), (2, "Grape")),
    "Liana": (1800, 1, (1, "Liana Seed"), (20, "Water")),
    "Motherboard": (1800, 1, (3, "Silicon"), (3, "Circuits"), (1, "Gold Bar")),
    "Polished Diamond": (60, 1, (5, "Diamond")),
    "Polished Ruby": (60, 1, (5, "Ruby")),
    "Polished Topaz": (60, 1, (5, "Topaz")),
    "Rubber": (1800, 1, (1, "Liana")),
    "Solid Propellant": (1200, 1, (3, "Rubber"), (10, "Aluminium")),
    "Steel Plate": (120, 1, (5, "Steel Bar")),
    "Sulfur Acid": (1800, 1, (2, "Sulfuf"), (1, "Clean Water")),
    "Grape": (1800, 2, (1, "Grape Seed"), (15, "Water")),
    "Accumulator": (180, 1, (20, "Sodium"), (20, "Sulfur")),
    "Gas Cylinder": (180, 1, (1, "Steel Plate"), (1, "Aluminium Tank"), (1, "Plastic Plate")),
    "Plastic Plate": (600, 1, (1, "Green Laser"), (50, "Coal"), (1, "Refined Oil")),
    "Polished Amethyst": (60, 1, (5, "Amethyst")),
    "Polished Sapphire": (60, 1, (5, "Sapphire")),
    "Refined Oil": (1800, 1, (10, "Oil"), (10, "Hydrogen"), (1, "Lab Flask")),
    "Solar Panel": (60, 1, (50, "Glass"), (10, "Silicon"), (1, "Rubber")),
    "Uranium Rod": (120, 1, (20, "Uranium"), (10, "Sodium")),
    "Bomb": (180, 1, (5, "Steel Bar"), (10, "Gundpowder")),
    "Diethyl Ether": (60, 1, (1, "Sulfur Acid"), (1, "Ethanol")),
    "Gear": (80, 1, (1, "Diamond Cutter"), (1, "Titanium Bar")),
    "Gunpowder": (120, 20, (1, "Diethyl Ether"), (2, "Sulfur Acid"), (2, "Tree")),
    "Polished Alexandrite": (60, 1, (5, "Alexandirte")),
    "Steel Pipe": (60, 1, (1, "Steel Plate")),
    "Titanium": (20, 50, (1, "Sulfur Acid"), (100, "Titanium Ore")),
    "Titanium Bar": (60, 1, (5, "Titanium")),
    "Compressor": (180, 1, (5, "Iron Bar"), (1, "Rubber"), (2, "Refined Oil")),
    "Liquid Nitrogen": (120, 4, (10, "Nitrogen"), (1, "Compressor"), (1, "Aluminium Bottel")),
    "Optic Fiber": (120, 10, (1, "Plastic Plate"), (10, "Oxygen"), (10, "Silikon")),
    "Oxygen Cylinder": (120, 1, (5, "Oxygen"), (10, "Silicon")),
    "Polished Obsidian": (60, 1, (5, "Obsidian")),
    "Sapphire Crystal Glass": (120, 1, (10, "Sapphire")),
    "Electrical Engine": (300, 1, (20, "Aluminium Bar"), (1, "Magnet"), (50, "Insulated Wire")),
    "LCD Monitor": (300, 1, (5, "Silikon"), (20, "Insulated Wire"), (5, "Sapphire Crystal Galss")),
    "Magnet": (120, 1, (1, "Magentite Bar")),
    "Enhanced Helium 3": (1800, 1, (1, "Aluminium Bottle"), (100, "Helium 3"), (1, "Compressor")),
    "Magnetite Bar": (60, 1, (5, "Magnetite Ore")),
    "Magnetite Ore": (360, 1, (1, "Iron Bar"), (5, "Oxygen"), (5, "Green Laser")),
}
deep_town_items_prices = {
    "Coal": 1,
    "Copper": 2,
    "Iron": 3,
    "Amber": 4,
    "Amber Charger": 4,
    "Water": 5,
    "Aluminium": 5,
    "Silver": 7,
    "Copper Nail": 7,
    "Tree Seed": 10,
    "Gold": 10,
    "Emerald": 12,
    "Platinum": 13,
    "Topaz": 14,
    "Mithril": 14,
    "Wire": 15,
    "Ruby": 15,
    "Graphite": 15,
    "Sapphire": 16,
    "Diamond": 18,
    "Amethyst": 18,
    "Titanium Ore": 19,
    "Alexandrite": 19,
    "Obsidian": 20,
    "Oil": 21,
    "Uranium": 22,
    "Copper Bar": 25,
    "Iron Bar": 40,
    "Pumpkin": 50,
    "Aluminium Bar": 50,
    "Aluminium Bottle": 55,
    "Polished Amber": 70,
    "Sulfur": 100,
    "Sodium Chloride": 100,
    "Sodium": 100,
    "Silicon": 100,
    "Defective Pumpkin": 100,
    "Cosmic Ice": 100,
    "Amber Insulation": 125,
    "Steel Bar": 150,
    "Polished Emerald": 160,
    "Tree": 193,
    "Silver Bar": 200,
    "Polished Topaz": 200,
    "Battery": 200,
    "Polished Sapphire": 230,
    "Polished Ruby": 250,
    "Polished Amethyst": 250,
    "Gold Bar": 250,
    "Titanium": 260,
    "Polished Alexandrite": 270,
    "Polished Obsidian": 280,
    "Amber Bracelet": 280,
    "Polished Diamond": 300,
    "Nitrogen": 300,
    "Copper Knife": 300,
    "Hydrogen": 400,
    "Helium 3": 400,
    "Green Laser": 400,
    "Mirror": 450,
    "Glass": 450,
    "Emerald Ring": 450,
    "Aluminium Tank": 450,
    "Lutetium Ore": 500,
    "Chlorine": 600,
    "Insulated Wire": 750,
    "Lamp": 760,
    "Lab Flask": 800,
    "Oxygen": 900,
    "Liana Seed": 1000,
    "Carved Pumpkin": 1100,
    "Grape Seed": 1200,
    "Clean Wate": 1200,
    "Grape": 1500,
    "Liana": 1700,
    "Steel Plate": 1800,
    "Ciruits": 2070,
    "Zip Drive": 2200,
    "Gunpowder": 2500,
    "Titanium Bar": 3000,
    "Sulfur Acid": 3500,
    "Rubber": 4000,
    "Ethanol": 4200,
    "Steel Pipe": 4300,
    "Seawater": 4900,
    "Zeolit": 5000,
    "Sapphire Crystal Glass": 5000,
    "Diamond Cutter": 5000,
    "Mirror Laser": 5400,
    "Maya Calendar": 6000,
    "Accumulator": 9000,
    "Optic Fiber": 10500,
    "Pine Seed": 11000,
    "Hydrochlorid Acid": 12000,
    "Magnetite Ore": 12500,
    "Liquid Nitrogen": 12500,
    "Lutetium": 13500,
    "Haircomb": 14000,
    "Refined Oil": 16500,
    "Uranium Rod": 17000,
    "Motherboard": 17000,
    "Diethyl Ether": 17000,
    "Gear": 18500,
    "Solid Propellant": 27000,
    "Gas Cylinder": 30000,
    "Obsidian Knife": 32000,
    "Pine Tree": 35000,
    "Plastic Plate": 40000,
    "Chipset": 40000,
    "Compressor": 44000,
    "Bomb": 55500,
    "Lutetium Bar": 68000,
    "Solar Panel": 69000,
    "LCD Monitor": 90000,
    "Nitrogen Tank": 110000,
    "Magnetite Bar": 137000,
    "Oxygen Cylinder": 173000,
    "Enhanced Helium 3": 190000,
    "Magnet": 300000,
    "Electrical Engine": 745000,
}
deep_town_raw_items = ("Copper",
                       "Iron",
                       "Aluminium",
                       "Coal",
                       "Amber",
                       "Water",
                       "Silver",
                       "Gold",
                       "Tree Seed",
                       "Emerald",
                       "Platinum",
                       "Topaz",
                       "Ruby",
                       "Sapphire",
                       "Amethyst",
                       "Diamond",
                       "Titanium Ore",
                       "Alexandirte",
                       "Obsidian",
                       "Oil",
                       "Uranium",
                       "Sodium",
                       "Sulfur",
                       "Silicon",
                       "Nitrogen",
                       "Helium 3",
                       "Lutetium Ore",
                       "Liana Seed",
                       "Grape Seed",)
