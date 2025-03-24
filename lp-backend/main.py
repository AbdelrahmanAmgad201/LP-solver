from DTOs.inputDTO import LinearSolverInput
from DTOs.outputDTO import SolverOutputDTO

from resources.tableauBuilder import TableauBuilder
from methods.twoPhaseMethod import TwoPhaseMethod
from engines.SimplexSolver import SimplexSolver
from engines.BigM import BigM

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import traceback

app = Flask(__name__)

# Enable CORS for all routes with all origins
CORS(app, supports_credentials=True)

@app.route('/solve', methods=['POST', 'OPTIONS'])
def solve():
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    try:
        json_data = request.get_json()
        if json_data is None:
            return jsonify({"error": "Invalid JSON or empty request body"}), 400
            
        json_str = json.dumps(json_data)
        
        # Debug - you can remove this after fixing
        print(f"Received data: {json_str}")
        
        # Your existing code...
        solver_input = LinearSolverInput.from_json(json_str)
        tableau = TableauBuilder.build_tableau(solver_input)
        output_dto = None
        
        # Method selection logic
        if solver_input.method == "twoPhase":
            pass
        elif solver_input.method == "goalProgramming":
            pass
        elif solver_input.method == "bigM":
            input = {
                "max": True if solver_input.optimization == "maximize" else False,
                "model": tableau,
                "obj_fun": solver_input.objective.coefficients
            }
            
            steps, cache, solution, message = BigM(input)
            output_dto = SolverOutputDTO(
                steps=steps,
                cache=cache,
                solution=solution,
                message=message
            )
        elif solver_input.method == "simplex":
            solver = SimplexSolver(
                tableau,
                solver_input.objective.coefficients,
                is_min=False if solver_input.optimization == "maximize" else True
            )
            steps, cache, solution, message = solver.solve()
            
            output_dto = SolverOutputDTO(
                steps=steps,
                cache=cache,
                solution=solution,
                message=message
            )
            
        result = jsonify(output_dto.to_dict())
        result.headers.add('Access-Control-Allow-Origin', '*')
        return result
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(traceback.format_exc())
        error_response = jsonify({"error": str(e), "traceback": traceback.format_exc()})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)