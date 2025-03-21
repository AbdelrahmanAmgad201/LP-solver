import json
from typing import List

class Constraint:
    def __init__(self, coefficients: List[int], operator: str, rhs: int):
        self.coefficients = coefficients
        self.operator = operator
        self.rhs = rhs

    @classmethod
    def from_dict(cls, data):
        return cls(data["coefficients"], data["operator"], data["rhs"])


class Objective:
    def __init__(self, coefficients: List[int]):
        self.coefficients = coefficients

    @classmethod
    def from_dict(cls, data):
        return cls(data["coefficients"])


class LinearSolverInput:
    def __init__(self, method: str, num_variables: int, num_constraints: int,
                 optimization: str, constraints: List[Constraint], objectives: List[Objective]):
        self.method = method
        self.num_variables = num_variables
        self.num_constraints = num_constraints
        self.optimization = optimization
        self.constraints = constraints
        self.objectives = objectives

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        constraints = [Constraint.from_dict(c) for c in data["constraints"]]
        objectives = [Objective.from_dict(o) for o in data["objectives"]]
        return cls(data["method"], data["numVariables"], data["numConstraints"],
                   data["optimization"], constraints, objectives)