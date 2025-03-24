from dataclasses import dataclass , asdict
from typing import List, Any, Dict
import numpy as np

@dataclass
class SolverOutputDTO:
    steps: List[str]
    cache: List[List[List[object]]]
    solution:List[List[object]]
    is_optimal: str
    optimal_value: float
    message: str = None

    def to_dict(self):
        def convert(obj):
            if isinstance(obj, (bool, int, float, str)):  # Primitive types
                return obj
            elif isinstance(obj, np.ndarray):  # Handle numpy arrays
                return obj.tolist()  # Convert numpy array to list
            elif isinstance(obj, list):  # Handle lists
                return [convert(item) for item in obj]
            elif isinstance(obj, dict):  # Handle dictionaries
                return {key: convert(value) for key, value in obj.items()}
            else:
                return str(obj)  # Convert other objects to strings

        data = asdict(self)
        return convert(data)