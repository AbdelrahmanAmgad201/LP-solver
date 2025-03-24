from DTOs.inputDTO import LinearSolverInput
from DTOs.outputDTO import SolverOutputDTO

from resources.tableauBuilder import TableauBuilder
from methods.twoPhaseMethod import TwoPhaseMethod
from engines.SimplexSolver import SimplexSolver
from engines.BigM import BigM

from flask import Flask,request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
@app.route('/solve', methods=['POST'])
def solve():
    json_data = request.get_json()
    json_str = json.dumps(json_data)
    solver_input = LinearSolverInput.from_json(json_str)
    tableau = TableauBuilder.build_tableau(solver_input)
    output_dto = None

    if solver_input.method == "twoPhase" :
        pass
    elif solver_input.method == "goalProgramming":
        pass
    
    elif solver_input.method == "bigM" :
        input = {"max" : True if solver_input.optimization == "maximize" else False
                ,"model" : tableau 
                ,"obj_fun" : solver_input.objective.coefficients} 
        steps, cache, solution, isOptimal, ans = BigM(input)
        output_dto = SolverOutputDTO(
            steps=steps,
            cache=cache,
            solution=solution,
            is_optimal="true" if isOptimal else "false",
            optimal_value=ans,
            message="Solution found successfully" if isOptimal else "No optimal solution found"
        )
        print("Output DTO created:", output_dto)
        
    elif solver_input.method == "simplex":
        solver = SimplexSolver(tableau,
                            solver_input.objective.coefficients,
                            is_min=False if solver_input.optimization == "maximize" else True)
        steps, cache, solution, isOptimal, ans = solver.solve()

        output_dto = SolverOutputDTO(
            steps=steps,
            cache=cache,
            solution=solution,
            is_optimal="true" if isOptimal else "false",
            optimal_value=ans,
            message="Solution found successfully" if isOptimal else "No optimal solution found"
        )
        
        
    return jsonify(output_dto.to_dict())   



if __name__ == '__main__':
    app.run(debug=True)