from src.objects import Manufacturer, Shop, Warehouse, Vegetable

"""Constant values, as well as concrete dataclass instances"""

WEEKS_PER_YEAR = 52
KILOS_PER_TON = 1000


weekly_demand_bounds = {
    # Weekly demand bounds for each vegetable in kilograms
    Vegetable.CARROT: (200, 400),
    Vegetable.CABBAGE: (100, 300),
    Vegetable.BEETROOT: (50, 200),
    Vegetable.POTATO: (300, 550),
}


def get_shops() -> list[Shop]:
    """Get the list of shops"""

    # In case we change the demand bounds, the internal warehouse capacity is recalculated on each run
    max_weekly_demand = 2 * sum(bounds[1] for bounds in weekly_demand_bounds.values())

    return [
        Shop(
            (52.23123538348719, 21.002334582862733),
            "Złota 44",
            int(1.2 * max_weekly_demand),
        ),
        Shop(
            (52.12982562283376, 21.069531384711578),
            "Aleja Komisji Edukacji Narodowej 14",
            int(1.1 * max_weekly_demand),
        ),
        Shop(
            (52.24921523643051, 21.059415840535483),
            "Mińska 25A",
            int(1.3 * max_weekly_demand),
        ),
        Shop(
            (52.21497524319214, 20.978488664418016),
            "Częstochowska 4/6",
            int(1.4 * max_weekly_demand),
        ),
        Shop(
            (52.23266813037208, 21.11443224907392),
            "Ostrobramska 71",
            int(1.25 * max_weekly_demand),
        ),
        Shop(
            (52.23673845375636, 21.036976869610385),
            "Bulwary B. Grzymały Siedleckiego",
            int(1.15 * max_weekly_demand),
        ),
        Shop(
            (52.17787696451111, 21.05353804734241),
            "Sardyńska 1",
            int(1.35 * max_weekly_demand),
        ),
        Shop(
            (52.257231606228096, 20.987110490415766),
            "Pamiętajcie o Ogrodach 4",
            int(1.45 * max_weekly_demand),
        ),
        Shop(
            (52.24282413331787, 20.9081047450922),
            "Gen. Tadeusza Pełczyńskiego 14",
            int(1.5 * max_weekly_demand),
        ),
        Shop(
            (52.209244900152974, 21.008531883983533),
            "Aleja Niepodległości 162",
            int(1.2 * max_weekly_demand),
        ),
    ]


def get_manufacturers() -> list[Manufacturer]:
    """Get the list of manufacturers"""
    manufacturers = [
        Manufacturer(
            (52.196210702994726, 20.623323179851976),
            "Błonie",
            {
                Vegetable.POTATO: 120 * KILOS_PER_TON,
                Vegetable.CABBAGE: 80 * KILOS_PER_TON,
                Vegetable.BEETROOT: 120 * KILOS_PER_TON,
                Vegetable.CARROT: 60 * KILOS_PER_TON,
            },
        ),
        Manufacturer(
            (52.07895991519026, 20.696598439808064),
            "Książenice",
            {
                Vegetable.POTATO: 60 * KILOS_PER_TON,
                Vegetable.CABBAGE: 90 * KILOS_PER_TON,
                Vegetable.BEETROOT: 150 * KILOS_PER_TON,
                Vegetable.CARROT: 50 * KILOS_PER_TON,
            },
        ),
        Manufacturer(
            (51.98163892918433, 21.211795297678236),
            "Góra Kalwaria",
            {
                Vegetable.POTATO: 160 * KILOS_PER_TON,
                Vegetable.CABBAGE: 70 * KILOS_PER_TON,
                Vegetable.BEETROOT: 190 * KILOS_PER_TON,
                Vegetable.CARROT: 90 * KILOS_PER_TON,
            },
        ),
        Manufacturer(
            (52.1152108196775, 21.269433923138475),
            "Otwock",
            {
                Vegetable.POTATO: 260 * KILOS_PER_TON,
                Vegetable.CABBAGE: 50 * KILOS_PER_TON,
                Vegetable.BEETROOT: 60 * KILOS_PER_TON,
                Vegetable.CARROT: 100 * KILOS_PER_TON,
            },
        ),
        Manufacturer(
            (52.357299338110245, 21.250353828893264),
            "Wołomin",
            {
                Vegetable.POTATO: 200 * KILOS_PER_TON,
                Vegetable.CABBAGE: 230 * KILOS_PER_TON,
                Vegetable.BEETROOT: 190 * KILOS_PER_TON,
                Vegetable.CARROT: 110 * KILOS_PER_TON,
            },
        ),
        Manufacturer(
            (52.40750915150292, 20.920774568903166),
            "Legionowo",
            {
                Vegetable.POTATO: 300 * KILOS_PER_TON,
                Vegetable.CABBAGE: 140 * KILOS_PER_TON,
                Vegetable.BEETROOT: 60 * KILOS_PER_TON,
                Vegetable.CARROT: 90 * KILOS_PER_TON,
            },
        ),
    ]

    return manufacturers


def get_warehouses() -> list[Warehouse]:
    """Get the list of warehouses"""

    return [
        Warehouse(
            (52.175584628053144, 20.793660692851642), "Pruszków", 800 * KILOS_PER_TON
        ),
        Warehouse(
            (52.095790995772646, 21.023008661957697), "Piaseczno", 1200 * KILOS_PER_TON
        ),
        Warehouse(
            (52.289563668216005, 21.235200160810102), "Zielonka", 750 * KILOS_PER_TON
        ),
    ]


def get_all_locations() -> tuple[list[Manufacturer], list[Shop], list[Warehouse]]:
    """Get all manuracturers, shops and warehouses."""
    return get_manufacturers(), get_shops(), get_warehouses()
