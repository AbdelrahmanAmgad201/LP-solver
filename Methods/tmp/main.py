from inputDTO import LinearSolverInput
from tableauBuilder import TableauBuilder
from twoPhaseMethod import TwoPhaseMethod
from SimplexSolver import SimplexSolver
from BigM import BigM
from outputDTO import SolverOutputDTO

from flask import Flask, jsonify

app = Flask(__name__)
@app.route('/solve', methods=['POST'])
def solve():
    json_str = request.json
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
        output_dto = SolverOutputDTO(
            steps=steps,
            cache=cache,
            solution=solution,
            is_optimal=isOptimal,
            optimal_value=ans,
            
        )
        """if not steps:
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
            print("Optimal Value:", ans)"""
    elif solver_input.method == "Simplex":
        solver = SimplexSolver(tableau,
                            solver_input.objectives[0].coefficients,
                            is_min=False if solver_input.optimization == "maximize" else True)
        steps, cache, solution, isOptimal, ans = solver.solve()

        output_dto = SolverOutputDTO(
            steps=steps,
            cache=cache,
            solution=solution,
            is_optimal=isOptimal,
            optimal_value=ans,

        )
        """if not steps:
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
            print("Optimal Value:", ans)"""
    return jsonify(output_dto.__dict__)   



if __name__ == '__main__':
    app.run(debug=True)