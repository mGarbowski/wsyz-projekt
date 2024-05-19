import pyomo.environ as pyo

model = pyo.AbstractModel()


# The vegetables
model.Products = pyo.Set(dimen=1)


# Number of weeks
model.NumWeeks = pyo.Param(within=pyo.NonNegativeIntegers)
model.Weeks = pyo.RangeSet(1, model.NumWeeks)


# The manufacturers and their yearly production capacity
model.Manufacturers = pyo.Set(dimen=1)
model.ManufacturerCapabilities = pyo.Param(
    model.Manufacturers, model.Products, within=pyo.NonNegativeIntegers
)

# The shops and their expected demand for each product in each week
model.Shops = pyo.Set(dimen=1)
model.ExpectedDemand = pyo.Param(
    model.Shops, model.Weeks, model.Products, within=pyo.NonNegativeIntegers
)
#  The on-site warehouse capacity of each shop
model.OnSiteWarehouseCapacity = pyo.Param(model.Shops, within=pyo.NonNegativeIntegers)
# The required "padding" for each product in each shop each week
model.MinimumStock = pyo.Param(
    model.Shops, model.Products, within=pyo.NonNegativeIntegers
)


# The warehouses and their capacity
model.Warehouses = pyo.Set(dimen=1)
model.WarehouseCapacity = pyo.Param(model.Warehouses, within=pyo.NonNegativeIntegers)


# Cost of transporting a ton of product by a kilometer
model.FuelPrice = pyo.Param(within=pyo.NonNegativeReals)

# Distances between locations
model.Distances = pyo.Param(model.Warehouses, model.Shops | model.Manufacturers)  # type: ignore

# TODO DEDUPLICATE
model.WarehouseShopDistances = pyo.Param(
    model.Warehouses, model.Shops, within=pyo.NonNegativeReals
)
model.WarehouseManufacturerDistances = pyo.Param(
    model.Warehouses, model.Manufacturers, within=pyo.NonNegativeReals
)

# Number of tons shipped from manufacturer to warehouses yearly
model.shipped_from_manufacturer = pyo.Var(
    model.Manufacturers,
    model.Warehouses,
    model.Products,
    within=pyo.NonNegativeIntegers,
)

# Number of kilos shipped from warehouses to shops weekly
model.shipped_from_warehouse = pyo.Var(
    model.Weeks,
    model.Warehouses,
    model.Shops,
    model.Products,
    within=pyo.NonNegativeIntegers,
)

# Leftover stock in the on-site warehouse after each week for each shop and product
model.leftover_stock = pyo.Var(
    model.Weeks,
    model.Shops,
    model.Products,
    within=pyo.NonNegativeIntegers,
)


# Constraints
def leftover_equality_constraint(model, shop, week, product):
    """Constraint that sets the value of leftover stock in the on-site warehouse after each week"""
    if week == 1:
        return model.leftover_stock[week, shop, product] == 0
    return (
        model.leftover_stock[week, shop, product]
        == model.leftover_stock[week - 1, shop, product]
        + model.shipped_from_warehouse[week, model.Warehouses[1], shop, product]
        - model.ExpectedDemand[shop, week, product]
    )


def manufacturing_capacity_constraint(model, manufacturer, product):
    """Constraint to ensure that the yearly production capacity of a manufacturer is not exceeded"""
    return (
        sum(
            model.shipped_from_manufacturer[manufacturer, warehouse, product]
            for warehouse in model.Warehouses
        )
        <= model.ManufacturerCapabilities[manufacturer, product]
    )


def warehouse_capacity_constraint(model, warehouse):
    """Constraint to ensure that the capacity of a warehouse is not exceeded"""
    return (
        sum(
            model.shipped_from_manufacturer[manufacturer, warehouse, product]
            for manufacturer in model.Manufacturers
            for product in model.Products
        )
        <= model.WarehouseCapacity[warehouse]
    )


def on_site_warehouse_capacity_constraint(model, shop, week):
    """Constraint to ensure that the capacity of the on-site warehouse is not exceeded"""
    if week == 1:
        return (
            sum(
                model.shipped_from_warehouse[week, warehouse, shop, product]
                for warehouse in model.Warehouses
                for product in model.Products
            )
            <= model.OnSiteWarehouseCapacity[shop]
        )
    return (
        sum(
            model.shipped_from_warehouse[week, warehouse, shop, product]
            for warehouse in model.Warehouses
            for product in model.Products
        )
        + sum(
            model.leftover_stock[week - 1, shop, product] for product in model.Products
        )
        <= model.OnSiteWarehouseCapacity[shop]
    )


def minimum_stock_constraint(model, shop, week, product):
    """Constraint to ensure that the minimum stock of a product in a shop is maintained"""
    if week == 1:
        return (
            sum(
                model.shipped_from_warehouse[week, warehouse, shop, product]
                for warehouse in model.Warehouses
            )
            >= model.MinimumStock[shop, product]
        )
    return (
        sum(
            model.shipped_from_warehouse[week, warehouse, shop, product]
            for warehouse in model.Warehouses
        )
        + model.leftover_stock[week - 1, shop, product]
        >= model.MinimumStock[shop, product]
    )


# # Add the defined constraints to the model

model.leftover_equality_constraint = pyo.Constraint(
    model.Shops, model.Weeks, model.Products, rule=leftover_equality_constraint
)

model.manufacturing_capacity_constraint = pyo.Constraint(
    model.Manufacturers, model.Products, rule=manufacturing_capacity_constraint
)
model.warehouse_capacity_constraint = pyo.Constraint(
    model.Warehouses, rule=warehouse_capacity_constraint
)

model.on_site_warehouse_capacity_constraint = pyo.Constraint(
    model.Shops, model.Weeks, rule=on_site_warehouse_capacity_constraint
)

model.minimum_stock_constraint = pyo.Constraint(
    model.Shops, model.Weeks, model.Products, rule=minimum_stock_constraint
)


# Objective function
def objective_function(model):
    """The objective function is to minimize the total cost of transportation"""
    return sum(
        model.FuelPrice
        * model.shipped_from_manufacturer[manufacturer, warehouse, product]
        * model.WarehouseManufacturerDistances[warehouse, manufacturer]
        for manufacturer in model.Manufacturers
        for warehouse in model.Warehouses
        for product in model.Products
    ) + sum(
        model.FuelPrice
        * model.shipped_from_warehouse[week, warehouse, shop, product]
        * model.WarehouseShopDistances[warehouse, shop]
        for week in model.Weeks
        for warehouse in model.Warehouses
        for shop in model.Shops
        for product in model.Products
    )


model.OBJ = pyo.Objective(rule=objective_function, sense=pyo.minimize)
