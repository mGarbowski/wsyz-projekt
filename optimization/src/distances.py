from dotenv import load_dotenv
import googlemaps
import pickle
import os

from instances import get_all_locations
from objects import Location, Manufacturer, Shop, Warehouse

load_dotenv()
DISTANCES_CACHE = "data/distances.pkl"


def get_distance(
    location1: Location, location2: Location, client: googlemaps.Client
) -> float:
    """Calculates the distance between two locations using the Google Maps API."""

    distance = client.distance_matrix(  # type: ignore
        location1.coordinates,
        location2.coordinates,
        mode="driving",
    )["rows"][0]["elements"][0]["distance"]["value"]

    # return the distance in kilometers
    return distance / 1000


def get_distances() -> dict[tuple[Warehouse, Shop | Manufacturer], float]:
    """Calculates the distances between the manufacturers, shops and warehouses. The distances are stored in a pickle file,
    if it's not found, the function makes google maps api requests. An API key needs to be passed
    via the .env API_KEY variable."""
    if os.path.exists(DISTANCES_CACHE):
        with open(DISTANCES_CACHE, "rb") as file:
            distances = pickle.load(file)
        return distances

    distances = {}
    manufacturers, shops, warehouses = get_all_locations()
    gmaps = googlemaps.Client(key=os.getenv("API_KEY"))

    for warehouse in warehouses:
        for location in shops + manufacturers:
            distances[(warehouse, location)] = get_distance(warehouse, location, gmaps)

    pickle.dump(distances, open(DISTANCES_CACHE, "wb"))

    return distances
