import pyomo.environ as pyo
from src.concrete import data
from src.abstract import model
from src.generate_tables import save_results_to_csv
from src.debugging import debug_instance

DEBUG_INSTANCE = False


def main():
    """Create an instance of the model and solve it"""
    instance = model.create_instance(data)
    opt = pyo.SolverFactory("cbc")
    results = opt.solve(instance, tee=DEBUG_INSTANCE)

    if DEBUG_INSTANCE:
        debug_instance(instance, results)  # type: ignore

    print(f"Objective function value: { round(pyo.value(instance.OBJ),2) } PLN")  # type: ignore
    save_results_to_csv(instance)


if __name__ == "__main__":
    main()
