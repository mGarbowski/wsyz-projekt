from instances import get_shops, get_warehouses, get_manufacturers
from distances import get_distances
from utils import get_weekly_demand, WEEKS_PER_YEAR, KILOS_PER_TON
from statistics import mean
from objects import Vegetable


manufacturers, shops, warehouses, distances, demand = (
    get_manufacturers(),
    get_shops(),
    get_warehouses(),
    get_distances(),
    get_weekly_demand(),
)

average_demand_by_shop = {
    (shop, vegetable): mean(
        demand[(shop, week, vegetable)] for week in range(1, WEEKS_PER_YEAR + 1)  # type: ignore
    )
    for vegetable in Vegetable
    for shop in shops
}
minimum_stock = {
    # 10% of average weekly demand per shop
    (shop, vegetable): int(0.1 * average_demand_by_shop[(shop, vegetable)])
    for vegetable in Vegetable
    for shop in shops
}


def pyo_mapping(v):
    """Transform a value into a mapping with a single None key, as this is the way
    to initialize params in pyomo"""
    return {None: v}


flat_manufacturer_capabilities = {
    # Flatten the manufacturer capabilities to fit the pyomo indexing
    (m, v): m.capabilities[v]
    for m in manufacturers
    for v in Vegetable
}

data = pyo_mapping(
    {
        "NumWeeks": pyo_mapping(WEEKS_PER_YEAR),
        "Products": [product for product in Vegetable],
        "Manufacturers": manufacturers,
        "Shops": shops,
        "Warehouses": warehouses,
        "Distances": distances,
        "ManufacturerCapabilities": flat_manufacturer_capabilities,
        "ExpectedDemand": demand,
        "OnSiteWarehouseCapacity": {
            shop: shop.on_site_warehouse_capacity for shop in shops
        },
        "MinimumStock": minimum_stock,
        "WarehouseCapacity": {w: w.capacity for w in warehouses},
        "FuelPrice": pyo_mapping(5 / KILOS_PER_TON),
    }
)