from inputDTO import LinearSolverInput
from tableauBuilder import TableauBuilder
from twoPhaseMethod import TwoPhaseMethod
def main():
    p1 = """
    {"method":"simplex", "numVariables":2, "numConstraints":3, "optimization":"minimize", 
    "constraints":
    [
        {"coefficients":[0.5,0.25], "operator":"<=", "rhs":4}, 
        {"coefficients":[1,3], "operator":">=", "rhs":20},
        {"coefficients":[1,1], "operator":"=", "rhs":10}
    ], 
    "objectives":[{"coefficients":[2,3]}]}
    """
    
    p2 = """
        {
            "method": "simplex",
            "numVariables": 2,
            "numConstraints": 3,
            "optimization": "minimize",
            "constraints": [
                {"coefficients": [3, 1], "operator": "=", "rhs": 3},
                {"coefficients": [4, 3], "operator": ">=", "rhs": 6},
                {"coefficients": [1, 2], "operator": "<=", "rhs": 4}
            ],
            "objectives": [
                {"coefficients": [4, 1]}
            ]
        }
    """
    solve(p1)


def solve(json_str):
    solver_input = LinearSolverInput.from_json(json_str)
    tableau = TableauBuilder.build_tableau(solver_input)
    print(tableau)
    msg, tableau = TwoPhaseMethod.phase_one(tableau)
    obj_fun = TableauBuilder.build_objective(tableau, solver_input)
    print(obj_fun)
    if msg == "optimal":
        TwoPhaseMethod.phase_two(tableau, obj_fun)

if __name__ == "__main__":
    main()