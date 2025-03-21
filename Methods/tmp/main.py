from inputDTO import LinearSolverInput
from tableauBuilder import TableauBuilder
from twoPhaseMethod import TwoPhaseMethod
from BigM import BigM

def main():
    p1 = """
    {"method":"twoPhase", "numVariables":2, "numConstraints":3, "optimization":"minimize", 
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
            "method": "BigM",
            "numVariables": 3,
            "numConstraints": 3,
            "optimization": "minimize",
            "constraints": [
                {"coefficients": [1, 1, 1], "operator": "<=", "rhs": 3},
                {"coefficients": [2, 1, 0], "operator": "<=", "rhs": 6},
                {"coefficients": [2, 1, 3], "operator": ">=", "rhs": 4}
            ],
            "objectives": [
                {"coefficients": [4, 4, 1]}
            ]
        }
    """
    solve(p2)


def solve(json_str):
    solver_input = LinearSolverInput.from_json(json_str)
    
    tableau = TableauBuilder.build_tableau(solver_input)
    
    if solver_input.method == "twoPhase" :
        msg, tableau = TwoPhaseMethod.phase_one(tableau)
        obj_fun = TableauBuilder.build_objective(tableau, solver_input)
        if msg == "optimal":
            TwoPhaseMethod.phase_two(tableau, obj_fun)
    elif solver_input.method == "BigM" :
        
        
        input = {"max" : True if solver_input.optimization == "maximize" else False
                ,"model" : tableau 
                ,"obj_fun" : solver_input.objectives[0].coefficients} 
        steps, cache, solution, isOptimal, ans = BigM(input)
        if not steps:
            print("No valid solution found.")
        else:
            print("Steps:")
            for step in steps:
                print(step)

            print("\nCache:")
            for i, iteration in enumerate(cache):
                print(f"Iteration {i+1}:")
                for row in iteration:
                    print("\t".join(map(str, row)))

            print("\nSolution:", solution)
            print("Is Optimal:", isOptimal)
            print("Optimal Value:", ans)
       



if __name__ == "__main__":
    main()