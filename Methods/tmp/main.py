from inputDTO import LinearSolverInput
from tableauBuilder import TableauBuilder
from twoPhaseMethod import TwoPhaseMethod
from SimplexSolver import SimplexSolver
from BigM import BigM
from outputDTO import SolverOutputDTO

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
    print(solver_input.method )
    output_dto = None
    if solver_input.method == "twoPhase" :
        msg, tableau = TwoPhaseMethod.phase_one(tableau)
        obj_fun = TableauBuilder.build_objective(tableau, solver_input)
        if msg == "optimal":
            TwoPhaseMethod.phase_two(tableau, obj_fun)
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
        print("Output DTO created:", output_dto)
        
    return jsonify(output_dto.to_dict())   



if __name__ == '__main__':
    app.run(debug=True)