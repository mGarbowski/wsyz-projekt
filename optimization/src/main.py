import pyomo.environ as pyo
from concrete import data
from abstract import model


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
    for v in instance.component_objects(pyo.Var, active=True):
        nametoprint = str(str(v.name))
        print("Variable ", nametoprint)
        for index in v:
            vtoprint = pyo.value(v[index])
            print("   ", index, vtoprint)


if __name__ == "__main__":
    main()
