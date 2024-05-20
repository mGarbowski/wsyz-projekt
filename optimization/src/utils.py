import pickle
import random
from instances import get_shops, weekly_demand_bounds
from objects import Shop, Vegetable
import os

DEMAND_FILE = "data/demand.pkl"
WEEKS_PER_YEAR = 52
KILOS_PER_TON = 1000


type Week = int
type Kilos = int


def generate_weekly_demand() -> dict[tuple[Shop, Week, Vegetable], Kilos]:
    """Generate random weekly demand for each vegetable in kilograms."""
    weeks = range(1, WEEKS_PER_YEAR + 1)
    shops = get_shops()
    return_value = dict()

    for shop in shops:
        for week in weeks:
            for vegetable in Vegetable:
                demand = random.randint(*weekly_demand_bounds[vegetable])
                return_value[(shop, week, vegetable)] = demand

    # Save the dictionary to a file using pickle
    with open(DEMAND_FILE, "wb") as file:
        pickle.dump(return_value, file)

    return return_value


def get_weekly_demand() -> dict[tuple[Shop, Week, Vegetable], Kilos]:
    """Load the weekly demand dictionary from a file."""
    if not os.path.exists(DEMAND_FILE):
        generate_weekly_demand()

    with open(DEMAND_FILE, "rb") as file:
        return_value = pickle.load(file)
    return return_value
