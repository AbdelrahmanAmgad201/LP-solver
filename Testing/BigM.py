import unittest
from Methods.BigM import BigM
import numpy as np
import pandas as pd

class TestBigM(unittest.TestCase):
    def test_simple_case(self):
        # Simple case with <= constraints
        input_data = {
            "max": True,
            "model": np.array([
                [2, 3, 1, 10],
                [4, 1, 2, 8],
                [-3, -4, 0, 0]
            ]),
            "sign": ["<=", "<="]
        }
        steps, cache, solution, isOptimal, ans = BigM(input_data)
        
        self.assertTrue(isOptimal)
        self.assertAlmostEqual(ans, 0.0)

    def test_unbounded_case(self):
        # Unbounded case with >= constraints
        input_data = {
            "max": True,
            "model": np.array([
                [1, -1, 1, 10],
                [-1, 1, 1, 10],
                [-1, 1, 0, 0]
            ]),
            "sign": [">=", ">="]
        }
        with self.assertRaises(ValueError):
            BigM(input_data)

    def test_infeasible_case(self):
       
        input_data = {
            "max": True,
            "model": np.array([
                [1, 1, 1, 5],
                [1, 1, 1, 10],
                [1, 2, 0, 0]
            ]),
            "sign": ["<=", ">="]
        }
        steps, cache, solution, isOptimal, ans = BigM(input_data)
        
        self.assertFalse(isOptimal)
        

    def test_degenerate_case(self):
        # Degenerate case with redundant constraints
        input_data = {
            "max": True,
            "model": np.array([
                [1, 1, 1, 5],
                [1, 1, 1, 5],
                [1, 2, 0, 0]
            ]),
            "sign": ["<=", "<="]
        }
        steps, cache, solution, isOptimal, ans = BigM(input_data)
        
       
        self.assertTrue(isOptimal)
        self.assertAlmostEqual(ans, 10.0)

    def test_multiple_constraints(self):
        # Case with multiple constraints and mixed signs
        input_data = {
            "max": True,
            "model": np.array([
                [1, 2, 1, 6],
                [2, 1, 1, 8],
                [-1, 1, 1, 4],
                [1, 1, 0, 0]
            ]),
            "sign": ["<=", "<=", ">="]
        }
        steps, cache, solution, isOptimal, ans = BigM(input_data)
        
        self.assertTrue(isOptimal)
        self.assertAlmostEqual(ans, 2.0)

    def test_minimization_case(self):
        # Minimization case with >= constraints
        input_data = {
            "max": False,
            "model": np.array([
                [1, 2, 1, 6],
                [2, 1, 1, 8],
                [1, 1, 0, 0]
            ]),
            "sign": [">=", ">="]
        }
        steps, cache, solution, isOptimal, ans = BigM(input_data)
       
        self.assertTrue(isOptimal)
        self.assertAlmostEqual(ans, 0.0)

    
    def test_all_equality_constraints(self):
        # Case with all equality constraints
        input_data = {
            "max": True,
            "model": np.array([
                [1, 1, 1, 5],
                [2, 1, 1, 8],
                [1, 2, 0, 0]
            ]),
            "sign":  ["=", "="]
        }
        steps, cache, solution, isOptimal, ans = BigM(input_data)
        
        self.assertTrue(isOptimal)
        self.assertAlmostEqual(ans, 7.0)

    def test_mixed_signs_and_equality(self):
        # Case with mixed signs and equality constraints
        input_data = {
            "max": True,
            "model": np.array([
                [1, 2, 1, 6],
                [2, 1, 1, 8],
                [-1, 1, 1, 4],
                [1, 1, 0, 0]
            ]),
            "sign": ["<=", "=", ">="]
        }
        steps, cache, solution, isOptimal, ans = BigM(input_data)
        
        self.assertFalse(isOptimal)
        

if __name__ == '__main__':
    unittest.main()