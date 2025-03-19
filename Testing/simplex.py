import unittest
from Methods.simplex import simplex
import numpy as np
import pandas as pd

class TestSimplex(unittest.TestCase):
    def test_simple_case(self):
        
        input_data = {
            "max": True,
            "model": np.array([
                [2, 3, 1, 10],
                [4, 1, 2, 8],
                [-3, -4, 0, 0]
            ]),
            "sign": ["<=", "<="]
        }
        steps, cache, solution, isOptimal, ans = simplex(input_data)
        
        self.assertTrue(isOptimal)
        self.assertAlmostEqual(ans, 0.0)


if __name__ == '__main__':
    unittest.main()