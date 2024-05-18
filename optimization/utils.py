import enum
import pickle

DEMAND_FILE = "data/demand.pkl"


class Vegetable(enum.Enum):
    POTATO = enum.auto()
    CABBAGE = enum.auto()
    BEETROOT = enum.auto()
    CARROT = enum.auto()


def load_weekly_demand() -> dict[int, list[dict[Vegetable, int]]]:
    """Load the weekly demand dictionary from a file."""
    with open("demand.pkl", "rb") as file:
        return_value = pickle.load(file)
    return return_value
