import json
from typing import List, Optional

class Constraint:
    def __init__(self, coefficients: List[int], operator: str, rhs: int):
        self.coefficients = coefficients or []
        self.operator = operator or ""
        self.rhs = rhs or 0

    @classmethod
    def from_dict(cls, data):
        return cls(
            coefficients=data.get("coefficients", []),
            operator=data.get("operator", ""),
            rhs=data.get("rhs", 0)
        )

class Objective:
    def __init__(self, coefficients: List[int]):
        self.coefficients = coefficients or []

    @classmethod
    def from_dict(cls, data):
        return cls(
            coefficients=data.get("coefficients", [])
        )

class Goal:
    def __init__(self, coefficients: List[int], operator: str, rhs: int):
        self.coefficients = coefficients or []
        self.operator = operator or ""
        self.rhs = rhs or 0

    @classmethod
    def from_dict(cls, data):
        return cls(
            coefficients=data.get("coefficients", []),
            operator=data.get("operator", ""),
            rhs=data.get("rhs", 0)
        )

class LinearSolverInput:
    def __init__(
        self, method: str, num_variables: int, num_constraints: int,
        num_goals: Optional[int] = None, optimization: Optional[str] = None, 
        constraints: Optional[List[Constraint]] = None, objective: Optional[Objective] = None, 
        goals: Optional[List[Goal]] = None, all_non_negative: Optional[bool] = None
    ):
        self.method = method or ""
        self.num_variables = num_variables or 0
        self.num_constraints = num_constraints or 0
        self.num_goals = num_goals or 0
        self.optimization = optimization or ""
        self.constraints = constraints or []
        self.objective = objective or Objective([])
        self.goals = goals or []
        self.all_non_negative = all_non_negative if all_non_negative is not None else False

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        
        constraints = [Constraint.from_dict(c) for c in data.get("constraints", [])]
        objective = Objective.from_dict(data.get("objective", {})) if "objective" in data else Objective([])
        goals = [Goal.from_dict(g) for g in data.get("goals", [])] if "goals" in data else []

        return cls(
            method=data.get("method", ""),
            num_variables=data.get("numVariables", 0),
            num_constraints=data.get("numConstraints", 0),
            num_goals=data.get("numGoals", 0),
            optimization=data.get("optimization", ""),
            constraints=constraints,
            objective=objective,
            goals=goals,
            all_non_negative=data.get("allNonNegative", False)
        )
