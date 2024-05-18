import enum
import pickle

DEMAND_FILE = "data/demand.pkl"


class Vegetable(enum.Enum):
    POTATO = enum.auto()
    CABBAGE = enum.auto()
    BEETROOT = enum.auto()
    CARROT = enum.auto()


weekly_demand_bounds = {
    # Weekly demand bounds for each vegetable in kilograms
    Vegetable.CARROT: (200, 400),
    Vegetable.CABBAGE: (100, 300),
    Vegetable.BEETROOT: (50, 200),
    Vegetable.POTATO: (300, 550),
}


def load_weekly_demand() -> dict[int, list[dict[Vegetable, int]]]:
    """Load the weekly demand dictionary from a file."""
    with open(DEMAND_FILE, "rb") as file:
        return_value = pickle.load(file)
    return return_value
