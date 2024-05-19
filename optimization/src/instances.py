from objects import Manufacturer, Shop, Warehouse, Vegetable
from statistics import mean

weekly_demand_bounds = {
    # Weekly demand bounds for each vegetable in kilograms
    Vegetable.CARROT: (200, 400),
    Vegetable.CABBAGE: (100, 300),
    Vegetable.BEETROOT: (50, 200),
    Vegetable.POTATO: (300, 550),
}


def get_shops() -> list[Shop]:
    """Get the list of shops"""

    # In case we change the demand bounds, the internal warehouse capacity will be recalculated
    average_weekly_demand = sum(
        mean(bounds) for bounds in weekly_demand_bounds.values()
    )

    return [
        Shop(
            (52.23123538348719, 21.002334582862733),
            "Złota 44",
            int(1.2 * average_weekly_demand),
        ),
        Shop(
            (52.12982562283376, 21.069531384711578),
            "Aleja Komisji Edukacji Narodowej 14",
            int(1.1 * average_weekly_demand),
        ),
        Shop(
            (52.24921523643051, 21.059415840535483),
            "Mińska 25A",
            int(1.3 * average_weekly_demand),
        ),
        Shop(
            (52.21497524319214, 20.978488664418016),
            "Częstochowska 4/6",
            int(1.4 * average_weekly_demand),
        ),
        Shop(
            (52.23266813037208, 21.11443224907392),
            "Ostrobramska 71",
            int(1.25 * average_weekly_demand),
        ),
        Shop(
            (52.23673845375636, 21.036976869610385),
            "Bulwary B. Grzymały Siedleckiego",
            int(1.15 * average_weekly_demand),
        ),
        Shop(
            (52.17787696451111, 21.05353804734241),
            "Sardyńska 1",
            int(1.35 * average_weekly_demand),
        ),
        Shop(
            (52.257231606228096, 20.987110490415766),
            "Pamiętajcie o Ogrodach 4",
            int(1.45 * average_weekly_demand),
        ),
        Shop(
            (52.24282413331787, 20.9081047450922),
            "Gen. Tadeusza Pełczyńskiego 14",
            int(1.5 * average_weekly_demand),
        ),
        Shop(
            (52.209244900152974, 21.008531883983533),
            "Aleja Niepodległości 162",
            int(0.9 * average_weekly_demand),
        ),
    ]


def get_manufacturers() -> list[Manufacturer]:
    """Get the list of manufacturers"""
    manufacturers = [
        Manufacturer(
            (52.196210702994726, 20.623323179851976),
            "Błonie",
            {
                Vegetable.POTATO: 120,
                Vegetable.CABBAGE: 80,
                Vegetable.BEETROOT: 120,
                Vegetable.CARROT: 60,
            },
        ),
        Manufacturer(
            (52.07895991519026, 20.696598439808064),
            "Książenice",
            {
                Vegetable.POTATO: 60,
                Vegetable.CABBAGE: 90,
                Vegetable.BEETROOT: 150,
                Vegetable.CARROT: 50,
            },
        ),
        Manufacturer(
            (51.98163892918433, 21.211795297678236),
            "Góra Kalwaria",
            {
                Vegetable.POTATO: 160,
                Vegetable.CABBAGE: 70,
                Vegetable.BEETROOT: 190,
                Vegetable.CARROT: 90,
            },
        ),
        Manufacturer(
            (52.1152108196775, 21.269433923138475),
            "Otwock",
            {
                Vegetable.POTATO: 260,
                Vegetable.CABBAGE: 50,
                Vegetable.BEETROOT: 60,
                Vegetable.CARROT: 100,
            },
        ),
        Manufacturer(
            (52.357299338110245, 21.250353828893264),
            "Wołomin",
            {
                Vegetable.POTATO: 200,
                Vegetable.CABBAGE: 230,
                Vegetable.BEETROOT: 190,
                Vegetable.CARROT: 110,
            },
        ),
        Manufacturer(
            (52.40750915150292, 20.920774568903166),
            "Legionowo",
            {
                Vegetable.POTATO: 300,
                Vegetable.CABBAGE: 140,
                Vegetable.BEETROOT: 60,
                Vegetable.CARROT: 90,
            },
        ),
    ]

    return manufacturers


def get_warehouses() -> list[Warehouse]:
    """Get the list of warehouses"""

    return [
        Warehouse((52.175584628053144, 20.793660692851642), "Pruszków", 800 * 1000),
        Warehouse((52.095790995772646, 21.023008661957697), "Piaseczno", 1200 * 1000),
        Warehouse((52.289563668216005, 21.235200160810102), "Zielonka", 750 * 1000),
    ]


def get_all_locations() -> tuple[list[Manufacturer], list[Shop], list[Warehouse]]:
    """Get all manuracturers, shops and warehouses."""
    return get_manufacturers(), get_shops(), get_warehouses()
