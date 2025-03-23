from dataclasses import dataclass
from typing import List, Any, Dict

@dataclass
class SolverOutputDTO:
    steps: List[str]
    cache: List[List[List[object]]]
    solution:List[List[object]]
    is_optimal: bool
    optimal_value: float
    message: str = None