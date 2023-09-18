from src.new.util.game.game_dataclasses import Item, Reciep, Player


def get_item(name: str) -> Item:
    """
    Finds all items matching the passed item name
    :param name: Name of the Item
    :return: Item or raises LookupError if multiple or none itmes
    matching to the passed item name where found
    """
    matched_item = []

    for item in items:
        if item.name == name:
            matched_item.append(item)

    if len(matched_item) != 1:
        print(f"Error, found multiple/none matches! Matches: {matched_item} for search: {name}")
        raise LookupError

    return matched_item[0]


def get_reciep(name: str) -> Reciep:
    """
    Finds all recieps matching the passed item name
    :param name: Name of the item
    :return: Reciep or raises LookupError if multiple or none reciepts
    matching to the passed item name where found
    """
    matched_recieps = []

    for reciep in recieps:
        if reciep.item.name == name:
            matched_recieps.append(reciep)

    if len(matched_recieps) != 1:
        print(f"Error, found multiple/none matches! Matches: {matched_recieps} for search: {name}")
        raise LookupError

    return matched_recieps[0]


items = [
    # -- Raw Items Smelting -- #
    Item("Coal", 1, True),
    Item("Copper", 2, True),
    Item("Iron", 3, True),
    Item("Aluminium", 5, True),
    Item("Silver", 7, True),
    Item("Gold", 10, True),

    # -- Raw Items Juwel Crafting -- #
    Item("Amber", 4, True),
    Item("Emerald", 12, True),
    Item("Topaz", 14, True),
    Item("Ruby", 15, True),
    Item("Sapphire", 16, True),
    Item("Amethyst", 18, True),
    Item("Diamond", 18, True),
    Item("Alexandrite", 19, True),
    Item("Obsidian", 20, True),

    # -- Raw Items Chemistry -- #
    Item("Water", 5, True),
    Item("Titanium Ore", 19, True),
    Item("Oil", 21, True),
    Item("Sodium Chloride", 100, True),
    Item("Silicon", 100, True),
    Item("Sodium", 100, True),
    Item("Sulfur", 100, True),
    Item("Nitrogen", 300, True),
    Item("Hydrogen", 400, True),
    Item("Helium 3", 400, True),
    Item("Lutetium Ore", 500, True),
    Item("Chlorine", 600, True),
    Item("Oxygen", 900, True),

    # -- Gardening Items -- #
    Item("Tree Seed", 10, True),
    Item("Tree", 193, False),
    Item("Liana Seed", 1000, True),
    Item("Grape Seed", 1200, True),
    Item("Grape", 1500, False),
    Item("Liana", 1700, False),
    Item("Pine Seed", 11_000, False),
    Item("Pine Tree", 35_000, False),

    # -- Others --#
    Item("Platinum", 13, True),
    Item("Uranium", 22, True),
    Item("Pumpkin", 50, True),
    Item("Cosmic Ice", 100, True),

    # -- Crafted Items -- #
    Item("Amber Charger", 4, False),
    Item("Copper Nail", 7, False),
    Item("Graphite", 15, False),
    Item("Wire", 15, False),
    Item("Copper Bar", 25, False),
    Item("Iron Bar", 40, False),
    Item("Aluminium Bar", 50, False),
    Item("Aluminium Bottle", 55, False),
    Item("Polished Amber", 70, False),
    Item("Defective Pumpkin", 100, False),
    Item("Amber Insulation", 125, False),
    Item("Steel Bar", 150, False),
    Item("Polished Emerald", 160, False),
    Item("Battery", 200, False),
    Item("Polished Topaz", 200, False),
    Item("Silver Bar", 200, False),
    Item("Polished Sapphire", 230, False),
    Item("Gold Bar", 250, False),
    Item("Polished Amethyst", 250, False),
    Item("Polished Ruby", 250, False),
    Item("Polished Alexandrite", 270, False),
    Item("Amber Bracelet", 280, False),
    Item("Polished Obsidian", 280, False),
    Item("Copper Knife", 300, False),
    Item("Polished Diamond", 300, False),
    Item("Green Laser", 400, False),
    Item("Aluminium Tank", 450, False),
    Item("Emerald Ring", 450, False),
    Item("Glass", 450, False),
    Item("Mirror", 450, False),
    Item("Insulated Wire", 750, False),
    Item("Lamp", 760, False),
    Item("Lab Flask", 800, False),
    Item("Carved Pumpkin", 1100, False),
    Item("Steel Plate", 1800, False),
    Item("Circuits", 2070, False),
    Item("Titanium Bar", 3000, False),
    Item("Steel Pipe", 4300, False),
    Item("Diamond Cutter", 5000, False),
    Item("Sapphire Crystal Glass", 5000, False),
    Item("Mirror Laser", 5400, False),
    Item("Maya Calendar", 6000, False),
    Item("Accumulator", 9000, False),
    Item("Optic Fiber", 10_500, False),
    Item("Haircomb", 14_000, False),
    Item("Motherboard", 17_000, False),
    Item("Gear", 18_500, False),
    Item("Dry Ice", 25_000, False),
    Item("Solid Propellant", 27_000, False),
    Item("Gas Cylinder", 30_000, False),
    Item("Obsidian Knife", 32_000, False),
    Item("Chipset", 40_000, False),
    Item("Primordial Soup", 40_000, False),
    Item("Compressor", 44_000, False),
    Item("Corona Discharge Tube", 49_000, False),
    Item("Bomb", 55_500, False),
    Item("Lutetium Bar", 68_000, False),
    Item("Solar Panel", 69_000, False),
    Item("LCD Monitor", 90_000, False),
    Item("Nitrogen Tank", 110_000, False),
    Item("Magnetite Bar", 137_000, False),
    Item("Oxygen Cylinder", 173_000, False),
    Item("Magnet", 300_000, False),
    Item("Electrical Engine", 745_000, False),

    # -- Chemical Items -- #
    Item("Titanium", 260, False),
    Item("Clean Water", 1200, False),
    Item("Gunpowder", 2500, False),
    Item("Sulfuric Acid", 3500, False),
    Item("Rubber", 4000, False),
    Item("Ethanol", 4200, False),
    Item("Seawater", 4900, False),
    Item("Flora Defender", 5000, False),
    Item("Zeolit", 5000, False),
    Item("Hydrochloric Acid", 12_000, False),
    Item("Liquid Nitrogen", 12_500, False),
    Item("Magnetite Ore", 12_500, False),
    Item("Lutetium", 13_500, False),
    Item("Refined Oil", 16_500, False),
    Item("Diethyl Ether", 17_000, False),
    Item("Uranium Rod", 17_000, False),
    Item("Plastic Plate", 40_000, False),
    Item("Toxic Bomb", 77_500, False),
    Item("Enhanced Helium 3", 190_000, False)
]
recieps = [
    Reciep(
        get_item("Magnetite Ore"),
        360,
        1,
        [
            (1, get_item("Iron Bar")),
            (5, get_item("Oxygen")),
            (5, get_item("Green Laser"))
        ]
    ),
    Reciep(
        get_item("Magnetite Bar"),
        60,
        1,
        [
            (5, get_item("Magnetite Ore"))
        ]
    ),
    Reciep(
        get_item("Enhanced Helium 3"),
        1800,
        1,
        [
            (1, get_item("Aluminium Bottle")),
            (100, get_item("Helium 3")),
            (1, get_item("Compressor"))
        ]
    ),
    Reciep(
        get_item("Magnet"),
        120,
        1,
        [
            (1, get_item("Magnetite Bar"))
        ]
    ),
    Reciep(
        get_item("LCD Monitor"),
        300,
        1,
        [
            (5, get_item("Silicon")),
            (20, get_item("Insulated Wire")),
            (5, get_item("Sapphire Crystal Glass"))
        ]
    ),
    Reciep(
        get_item("Electrical Engine"),
        300,
        1,
        [
            (20, get_item("Aluminium Bar")),
            (1, get_item("Magnet")),
            (50, get_item("Insulated Wire"))
        ]
    ),
    Reciep(
        get_item("Sapphire Crystal Glass"),
        120,
        1,
        [
            (10, get_item("Sapphire"))
        ]
    ),
    Reciep(
        get_item("Polished Obsidian"),
        60,
        1,
        [
            (5, get_item("Obsidian"))
        ]
    ),
    Reciep(
        get_item("Oxygen Cylinder"),
        120,
        1,
        [
            (5, get_item("Oxygen")),
            (10, get_item("Silicon"))
        ]
    ),
    Reciep(
        get_item("Optic Fiber"),
        120,
        10,
        [
            (1, get_item("Plastic Plate")),
            (10, get_item("Oxygen")),
            (10, get_item("Silicon"))
        ]
    ),
    Reciep(
        get_item("Liquid Nitrogen"),
        120,
        4,
        [
            (10, get_item("Nitrogen")),
            (1, get_item("Compressor")),
            (1, get_item("Aluminium Bottle"))
        ]
    ),
    Reciep(
        get_item("Compressor"),
        180,
        1,
        [
            (5, get_item("Iron Bar")),
            (1, get_item("Rubber")),
            (2, get_item("Refined Oil"))
        ]
    ),
    Reciep(
        get_item("Titanium Bar"),
        60,
        1,
        [
            (5, get_item("Titanium"))
        ]
    ),
    Reciep(
        get_item("Titanium"),
        20,
        50,
        [
            (1, get_item("Sulfuric Acid")),
            (100, get_item("Titanium Ore"))
        ]
    ),
    Reciep(
        get_item("Steel Pipe"),
        60,
        1,
        [
            (1, get_item("Steel Plate"))
        ]
    ),
    Reciep(
        get_item("Polished Alexandrite"),
        60,
        1,
        [
            (5, get_item("Alexandrite"))
        ]
    ),
    Reciep(
        get_item("Gunpowder"),
        120,
        20,
        [
            (1, get_item("Diethyl Ether")),
            (2, get_item("Sulfuric Acid")),
            (2, get_item("Tree"))
        ]
    ),
    Reciep(
        get_item("Gear"),
        80,
        1,
        [
            (1, get_item("Diamond Cutter")),
            (1, get_item("Titanium Bar"))
        ]
    ),
    Reciep(
        get_item("Diethyl Ether"),
        60,
        1,
        [
            (1, get_item("Sulfuric Acid")),
            (1, get_item("Ethanol"))
        ]
    ),
    Reciep(
        get_item("Bomb"),
        180,
        1,
        [
            (5, get_item("Steel Bar")),
            (10, get_item("Gunpowder"))
        ]
    ),
    Reciep(
        get_item("Uranium Rod"),
        120,
        1,
        [
            (20, get_item("Uranium")),
            (10, get_item("Sodium"))
        ]
    ),
    Reciep(
        get_item("Solar Panel"),
        120,
        1,
        [
            (50, get_item("Glass")),
            (10, get_item("Silicon")),
            (1, get_item("Rubber"))
        ]
    ),
    Reciep(
        get_item("Refined Oil"),
        1800,
        1,
        [
            (10, get_item("Oil")),
            (10, get_item("Hydrogen")),
            (1, get_item("Lab Flask"))
        ]
    ),
    Reciep(
        get_item("Polished Sapphire"),
        60,
        1,
        [
            (5, get_item("Sapphire"))
        ]
    ),
    Reciep(
        get_item("Polished Amethyst"),
        60,
        1,
        [
            (5, get_item("Amethyst"))
        ]
    ),
    Reciep(
        get_item("Plastic Plate"),
        600,
        1,
        [
            (1, get_item("Green Laser")),
            (50, get_item("Coal")),
            (1, get_item("Refined Oil"))
        ]
    ),
    Reciep(
        get_item("Gas Cylinder"),
        180,
        1,
        [
            (1, get_item("Steel Plate")),
            (1, get_item("Aluminium Tank")),
            (1, get_item("Plastic Plate"))
        ]
    ),
    Reciep(
        get_item("Accumulator"),
        180,
        1,
        [
            (20, get_item("Sodium")),
            (20, get_item("Sulfur"))
        ]
    ),
    Reciep(
        get_item("Grape"),
        1800,
        2,
        [
            (1, get_item("Grape Seed")),
            (15, get_item("Water"))
        ]
    ),
    Reciep(
        get_item("Sulfuric Acid"),
        1800,
        1,
        [
            (2, get_item("Sulfur")),
            (1, get_item("Clean Water"))
        ]
    ),
    Reciep(
        get_item("Steel Plate"),
        120,
        1,
        [
            (5, get_item("Steel Bar"))
        ]
    ),
    Reciep(
        get_item("Solid Propellant"),
        1200,
        1,
        [
            (3, get_item("Rubber")),
            (10, get_item("Aluminium Bar"))
        ]
    ),
    Reciep(
        get_item("Rubber"),
        1800,
        1,
        [
            (1, get_item("Liana"))
        ]
    ),
    Reciep(
        get_item("Polished Topaz"),
        60,
        1,
        [
            (5, get_item("Topaz"))
        ]
    ),
    Reciep(
        get_item("Polished Ruby"),
        60,
        1,
        [
            (5, get_item("Ruby"))
        ]
    ),
    Reciep(
        get_item("Polished Diamond"),
        60,
        1,
        [
            (5, get_item("Diamond"))
        ]
    ),
    Reciep(
        get_item("Motherboard"),
        1800,
        1,
        [
            (3, get_item("Silicon")),
            (3, get_item("Circuits")),
            (1, get_item("Gold Bar"))
        ]
    ),
    Reciep(
        get_item("Liana"),
        1800,
        1,
        [
            (1, get_item("Liana Seed")),
            (20, get_item("Water"))
        ]
    ),
    Reciep(
        get_item("Ethanol"),
        1800,
        1,
        [
            (1, get_item("Aluminium Bottle")),
            (2, get_item("Grape"))
        ]
    ),
    Reciep(
        get_item("Diamond Cutter"),
        30,
        1,
        [
            (5, get_item("Polished Diamond")),
            (1, get_item("Steel Plate"))
        ]
    ),
    Reciep(
        get_item("Green Laser"),
        20,
        5,
        [
            (1, get_item("Lamp")),
            (1, get_item("Insulated Wire")),
            (1, get_item("Polished Emerald"))
        ]
    ),
    Reciep(
        get_item("Polished Emerald"),
        30,
        1,
        [
            (5, get_item("Emerald"))
        ]
    ),
    Reciep(
        get_item("Polished Amber"),
        30,
        1,
        [
            (5, get_item("Amber"))
        ]
    ),
    Reciep(
        get_item("Gold Bar"),
        60,
        1,
        [
            (5, get_item("Gold"))
        ]
    ),
    Reciep(
        get_item("Steel Bar"),
        45,
        1,
        [
            (1, get_item("Graphite")),
            (1, get_item("Iron Bar"))
        ]
    ),
    Reciep(
        get_item("Silver Bar"),
        60,
        1,
        [
            (5, get_item("Silver"))
        ]
    ),
    Reciep(
        get_item("Mirror Laser"),
        120,
        2,
        [
            (3, get_item("Mirror")),
            (1, get_item("Lamp")),
            (1, get_item("Battery"))
        ]
    ),
    Reciep(
        get_item("Mirror"),
        120,
        2,
        [
            (1, get_item("Silver Bar")),
            (1, get_item("Glass"))
        ]
    ),
    Reciep(
        get_item("Aluminium Tank"),
        120,
        5,
        [
            (3, get_item("Aluminium Bar"))
        ]
    ),
    Reciep(
        get_item("Aluminium Bar"),
        15,
        1,
        [
            (5, get_item("Aluminium"))
        ]
    ),
    Reciep(
        get_item("Insulated Wire"),
        200,
        1,
        [
            (1, get_item("Amber")),
            (1, get_item("Wire"))
        ]
    ),
    Reciep(
        get_item("Amber Insulation"),
        20,
        1,
        [
            (1, get_item("Aluminium Bottle")),
            (10, get_item("Amber"))
        ]
    ),
    Reciep(
        get_item("Amber Charger"),
        5,
        1,
        [
            (1, get_item("Amber"))
        ]
    ),
    Reciep(
        get_item("Aluminium Bottle"),
        30,
        1,
        [
            (1, get_item("Aluminium Bar"))
        ]
    ),
    Reciep(
        get_item("Lamp"),
        80,
        1,
        [
            (20, get_item("Graphite")),
            (10, get_item("Wire")),
            (5, get_item("Copper Bar"))
        ]
    ),
    Reciep(
        get_item("Lab Flask"),
        60,
        1,
        [
            (1, get_item("Glass"))
        ]
    ),
    Reciep(
        get_item("Hydrogen"),
        900,
        2,
        [
            (1, get_item("Clean Water"))
        ]
    ),
    Reciep(
        get_item("Glass"),
        60,
        1,
        [
            (2, get_item("Silicon"))
        ]
    ),
    Reciep(
        get_item("Clean Water"),
        600,
        1,
        [
            (1, get_item("Lab Flask")),
            (1, get_item("Water"))
        ]
    ),
    Reciep(
        get_item("Circuits"),
        180,
        1,
        [
            (20, get_item("Copper Bar")),
            (10, get_item("Iron Bar")),
            (50, get_item("Graphite"))
        ]
    ),
    Reciep(
        get_item("Battery"),
        120,
        1,
        [
            (5, get_item("Copper Bar")),
            (1, get_item("Iron Bar")),
            (1, get_item("Amber"))
        ]
    ),
    Reciep(
        get_item("Wire"),
        30,
        5,
        [
            (1, get_item("Copper Bar"))
        ]
    ),
    Reciep(
        get_item("Tree"),
        1800,
        10,
        [
            (1, get_item("Tree Seed")),
            (10, get_item("Water"))
        ]
    ),
    Reciep(
        get_item("Obsidian Knife"),
        120,
        1,
        [
            (50, get_item("Polished Obsidian")),
            (2, get_item("Tree")),
            (1, get_item("Silver Bar"))
        ]
    ),
    Reciep(
        get_item("Maya Calendar"),
        120,
        1,
        [
            (10, get_item("Gold Bar")),
            (2, get_item("Silver Bar"))
        ]
    ),
    Reciep(
        get_item("Iron Bar"),
        15,
        1,
        [
            (5, get_item("Iron"))
        ]
    ),
    Reciep(
        get_item("Haircomb"),
        120,
        1,
        [
            (10, get_item("Polished Alexandrite")),
            (15, get_item("Polished Amethyst")),
            (1, get_item("Silver Bar"))
        ]
    ),
    Reciep(
        get_item("Graphite"),
        5,
        1,
        [
            (5, get_item("Coal"))
        ]
    ),
    Reciep(
        get_item("Emerald Ring"),
        300,
        1,
        [
            (1, "Polished Emerald"),
            (1, "Gold Bar")
        ]
    ),
    Reciep(
        get_item("Copper Nail"),
        20,
        1,
        [
            (1, get_item("Copper Bar"))
        ]
    ),
    Reciep(
        get_item("Copper Bar"),
        10,
        1,
        [
            (5, get_item("Copper"))
        ]
    ),
    Reciep(
        get_item("Amber Bracelet"),
        120,
        1,
        [
            (1, get_item("Polished Amber")),
            (1, get_item("Silver Bar"))
        ]
    )
]
