""" Running this script regenerates all of the data files"""

import pickle
import random
from utils import *


def generate_weekly_demand() -> dict[int, list[dict[Vegetable, int]]]:
    """Generate random weekly demand for each vegetable in kilograms."""
    WEEKS_PER_YEAR = 52
    shops = range(10)
    return_value: dict[int, list[dict[Vegetable, int]]] = {i: [] for i in shops}

    for shop in shops:
        weekly_demand = [{} for _ in range(WEEKS_PER_YEAR)]
        for week in range(WEEKS_PER_YEAR):
            for vegetable in Vegetable:
                lower_bound, upper_bound = weekly_demand_bounds[vegetable]
                weekly_demand[week][vegetable] = random.randint(
                    lower_bound, upper_bound
                )
        return_value[shop] = weekly_demand

    # Save the dictionary to a file using pickle
    with open(DEMAND_FILE, "wb") as file:
        pickle.dump(return_value, file)

    return return_value


def main():
    generate_weekly_demand()


if __name__ == "__main__":
    main()
