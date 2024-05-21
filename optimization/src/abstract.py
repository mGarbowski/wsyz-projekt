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
model.Distances = pyo.Param(model.Warehouses, model.Manufacturers | model.Shops)  # type: ignore

# Number of kilos shipped from manufacturer to warehouses yearly
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


def leftover_equality_constraint(model, shop, week, product):
    """Constraint that sets the value of leftover stock in the on-site warehouse after each week"""
    if week == 1:
        return model.leftover_stock[week, shop, product] == 0
    return (
        model.leftover_stock[week - 1, shop, product]
        + sum(
            model.shipped_from_warehouse[week, warehouse, shop, product]
            for warehouse in model.Warehouses
        )
        - model.ExpectedDemand[shop, week, product]
        == model.leftover_stock[week, shop, product]
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
            # No week 0, edge case
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
            # Yes week -1, no edge case
            model.leftover_stock[week - 1, shop, product]
            for product in model.Products
        )
        <= model.OnSiteWarehouseCapacity[shop]
    )


def shipment_relation_constraint(model, warehouse, product):
    """Constraint to ensure that the shipments from warehouses to shops are related to the shipments from manufacturers to warehouses"""
    return sum(
        model.shipped_from_warehouse[week, warehouse, shop, product]
        for week in model.Weeks
        for shop in model.Shops
    ) <= sum(
        model.shipped_from_manufacturer[manufacturer, warehouse, product]
        for manufacturer in model.Manufacturers
    )


def demand_met_constraint(model, shop, week, product):
    """Constraint to ensure that the demand for a product in a shop is met"""
    if week == 1:
        return (
            sum(
                model.shipped_from_warehouse[week, warehouse, shop, product]
                for warehouse in model.Warehouses
            )
            >= model.ExpectedDemand[shop, week, product]
            + model.MinimumStock[shop, product]
        )
    return (
        sum(
            model.shipped_from_warehouse[week, warehouse, shop, product]
            for warehouse in model.Warehouses
        )
        + model.leftover_stock[week - 1, shop, product]
        >= model.ExpectedDemand[shop, week, product] + model.MinimumStock[shop, product]
    )


# Add the defined constraints to the model

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

model.demand_met_constraint = pyo.Constraint(
    model.Shops, model.Weeks, model.Products, rule=demand_met_constraint
)

model.shipment_relation_constraint = pyo.Constraint(
    model.Warehouses,
    model.Products,
    rule=shipment_relation_constraint,
)


# Objective function
def objective_function(model):
    """The objective function is to minimize the total cost of transportation"""
    return sum(
        # Cost of transporting from manufacturers to warehouses
        model.FuelPrice
        * model.shipped_from_manufacturer[manufacturer, warehouse, product]
        * model.Distances[warehouse, manufacturer]
        for manufacturer in model.Manufacturers
        for warehouse in model.Warehouses
        for product in model.Products
    ) + sum(
        # Cost of transporting from warehouses to shops
        model.FuelPrice
        * model.shipped_from_warehouse[week, warehouse, shop, product]
        * model.Distances[warehouse, shop]
        for week in model.Weeks
        for warehouse in model.Warehouses
        for shop in model.Shops
        for product in model.Products
    )


# Assign the objective function to the model
model.OBJ = pyo.Objective(rule=objective_function, sense=pyo.minimize)
