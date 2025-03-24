import json
from typing import List, Optional

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


class Goal:
    def __init__(self, coefficients: List[int], operator: str, rhs: int):
        self.coefficients = coefficients
        self.operator = operator
        self.rhs = rhs

    @classmethod
    def from_dict(cls, data):
        return cls(data["coefficients"], data["operator"], data["rhs"])


class LinearSolverInput:
    def __init__(self, method: str, num_variables: int, num_constraints: int,
                 num_goals: Optional[int] = None, optimization: Optional[str] = None, 
                 constraints: List[Constraint] = [], objectives: Optional[List[Objective]] = None, 
                 goals: Optional[List[Goal]] = None):
        self.method = method
        self.num_variables = num_variables
        self.num_constraints = num_constraints
        self.num_goals = num_goals
        self.optimization = optimization
        self.constraints = constraints
        self.objectives = objectives or []
        self.goals = goals or []

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        constraints = [Constraint.from_dict(c) for c in data.get("constraints", [])]
        objectives = [Objective.from_dict(o) for o in data.get("objectives", [])] if "objectives" in data else None
        goals = [Goal.from_dict(g) for g in data.get("goals", [])] if "goals" in data else None

        return cls(
            method=data["method"],
            num_variables=data["numVariables"],
            num_constraints=data["numConstraints"],
            num_goals=data.get("numGoals"),
            optimization=data.get("optimization"),
            constraints=constraints,
            objectives=objectives,
            goals=goals
        )
