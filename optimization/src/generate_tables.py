import pandas as pd
import pyomo.environ as pyo

WAREHOUSE_SHIPMENTS_CSV = "output/warehouse_shipments.csv"
MANUFACTURER_SHIPMENTS_CSV = "output/manufacturer_shipments.csv"


def deflatten_warehouse_shipments(warehouse_shipments: pyo.Var) -> dict:
    """Deflatten the warehouse shipments into a nested dictionary with keys (warehouse, week), (shop, product)"""
    rv = {}
    for index in warehouse_shipments:
        week, warehouse, shop, product = index  # type: ignore
        if (str(warehouse), week) not in rv:
            rv[str(warehouse), week] = {}
        rv[str(warehouse), week][str(shop), product.name] = pyo.value(
            warehouse_shipments[index]
        )

    return rv


def deflatten_manufacturer_shipments(manufacturer_shipments: pyo.Var) -> dict:
    """Deflatten the manufacturer shipments into a nested dictionary with keys (manufacturer, warehouse), product"""
    rv = {}
    for index in manufacturer_shipments:
        manufacturer, warehouse, product = index  # type: ignore
        if key := (str(manufacturer), str(warehouse)) not in rv:
            rv[key] = {}
        rv[key][product.name] = pyo.value(manufacturer_shipments[index])

    return rv


def deflatten_leftover_products(leftover_products: pyo.Var) -> dict:
    """Deflatten the leftover products into a nested dictionary with keys (shop, week) and product"""
    rv = {}
    for index in leftover_products:
        week, shop, product = index  # type: ignore
        if (key := (str(shop), week)) not in rv:
            rv[key] = {}
        if product.name not in rv[key]:
            rv[key][product.name] = {}
        rv[key][product.name] = pyo.value(leftover_products[index])
    return rv


def save_to_csv(
    warehouse_shipments: dict, manufacturer_shipments: dict, leftover_stock: dict
):
    """Save the warehouse and manufacturer shipments to a CSV file"""
    warehouse_shipments_df = pd.DataFrame(warehouse_shipments).T
    warehouse_shipments_df.to_csv(WAREHOUSE_SHIPMENTS_CSV)
    manufacturer_shipments_df = pd.DataFrame(manufacturer_shipments).T
    manufacturer_shipments_df.to_csv(MANUFACTURER_SHIPMENTS_CSV)
    leftover_stock_df = pd.DataFrame(leftover_stock).T
    leftover_stock_df.to_csv("output/leftover_stock.csv")


def save_results_to_csv(instance: pyo.Model):
    """Save the results of a model to a CSV file"""
    warehouse_shipments = deflatten_warehouse_shipments(instance.shipped_from_warehouse)  # type: ignore
    manufacturer_shipments = deflatten_manufacturer_shipments(
        instance.shipped_from_manufacturer  # type: ignore
    )
    leftover_stock = deflatten_leftover_products(instance.leftover_stock)  # type: ignore
    save_to_csv(warehouse_shipments, manufacturer_shipments, leftover_stock)
