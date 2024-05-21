import pyomo.environ as pyo
from src.concrete import data
from src.abstract import model
from src.generate_tables import save_results_to_csv
from pprint import pprint


def main():
    """Create an instance of the model and solve it"""
    instance = model.create_instance(data)
    opt = pyo.SolverFactory("cbc")
    results = opt.solve(instance, tee=True)
    print(results)

    # Print the parameter values
    for parmobject in instance.component_objects(pyo.Param, active=True):
        nametoprint = str(str(parmobject.name))
        print("Parameter ", nametoprint)
        for index in parmobject:
            vtoprint = pyo.value(parmobject[index])
            print("   ", index, vtoprint)

    # Print the variable values
    # for v in instance.component_objects(pyo.Var, active=True):
    #     nametoprint = str(str(v.name))
    #     print("Variable ", nametoprint)
    #     for index in v:
    #         vtoprint = pyo.value(v[index])
    #         print("   ", index, vtoprint)
    save_results_to_csv(instance)

    print("Warehouse capacity limits: ")
    pprint(
        {
            str(index): instance.WarehouseCapacity[index]  # type: ignore
            for index in instance.WarehouseCapacity  # type: ignore
        }
    )
    print("Sum of product shipped from manufacturer to warehouses:")
    pprint(
        {
            str(warehouse): sum(
                pyo.value(
                    instance.shipped_from_manufacturer[manufacturer, warehouse, product]  # type: ignore
                )
                for manufacturer in instance.Manufacturers  # type: ignore
                for product in instance.Products  # type: ignore
            )
            for warehouse in instance.Warehouses  # type: ignore
        }
    )

    print("Sum of product shipped from warehouse to shop:")
    pprint(
        sum(  # type: ignore
            pyo.value(instance.shipped_from_warehouse[week, warehouse, shop, product])  # type: ignore
            for week in instance.Weeks  # type: ignore
            for warehouse in instance.Warehouses  # type: ignore
            for shop in instance.Shops  # type: ignore
            for product in instance.Products  # type: ignore
        )
    )

    print("Sum of the demand")
    pprint(
        sum(  # type: ignore
            pyo.value(instance.ExpectedDemand[shop, week, product])  # type: ignore
            for shop in instance.Shops  # type: ignore
            for week in instance.Weeks  # type: ignore
            for product in instance.Products  # type: ignore
        )
    )

    print("Sum of all shipments from manufacturers to shops")
    print(
        sum(
            pyo.value(instance.shipped_from_manufacturer[manufacturer, warehouse, product])  # type: ignore
            for manufacturer in instance.Manufacturers  # type: ignore
            for warehouse in instance.Warehouses  # type: ignore
            for product in instance.Products  # type: ignore
        )
    )

    print("Manufacturer limits")
    pprint(
        {
            str(index): index.capabilities  # type: ignore
            for index in instance.Manufacturers  # type: ignore
        }
    )


if __name__ == "__main__":
    main()
