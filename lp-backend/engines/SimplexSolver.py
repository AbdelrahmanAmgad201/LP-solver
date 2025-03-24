import numpy as np

class SimplexSolver:
    def __init__(self, tableau, z, is_min=False):
        self.tableau = np.array([row[1:] for row in tableau[1:]], dtype=float)
        self.basic_vars = [row[0] for row in tableau[1:]]
        self.headers = tableau[0]
        self.z = np.array(z + [0] * (len(self.tableau[0]) - len(z)), dtype=float)  # Add zeros to match tableau width
        self.is_min = is_min
        self.steps = []
        self.iterations = []
        
        if is_min:
            self.z = -self.z  
        
       
        self.tableau = np.vstack([self.tableau, self.z])  

    def solve(self):
        cache = []
        self.basic_vars.append('z')
        while True:
            cache.append([self.headers] + [[self.basic_vars[i]] + list(self.tableau[i]) for i in range(len(self.tableau))])
            
            if np.all(self.tableau[-1, :-1] >= 0 if not self.is_min else self.tableau[-1, :-1] <= 0):
                break
            
            entering = np.argmin(self.tableau[-1, :-1]) if not self.is_min else np.argmax(self.tableau[-1, :-1])
            valid_rows = self.tableau[:-1, entering] > 0
            ratios = np.full_like(self.tableau[:-1, -1], np.inf, dtype=float)
            ratios[valid_rows] = self.tableau[:-1, -1][valid_rows] / self.tableau[:-1, entering][valid_rows]
            
            if np.all(ratios == np.inf):
                return [], [], [],"The problem is unbounded."
            
            leaving = np.argmin(ratios)
            self.steps.append(f"Pivot on row {self.basic_vars[leaving]} (leaving), column {self.headers[entering+1]} (entering)")
            self.basic_vars[leaving] = self.headers[entering + 1]
            pivot_element = self.tableau[leaving, entering]
            self.tableau[leaving] /= pivot_element
            for i in range(len(self.tableau)):
                if i != leaving:
                    self.tableau[i] -= self.tableau[i, entering] * self.tableau[leaving]
        
        solution = np.zeros(self.tableau.shape[1])
        for i in range(len(self.basic_vars)):
            if self.basic_vars[i] in self.headers:
                solution[self.headers.index(self.basic_vars[i]) - 1] = self.tableau[i, -1]
        
        optimal_value = self.tableau[-1, -1]
        
        return self.steps, cache, [[solution[:-1]] + [self.headers[1:-1]]], f"Optimization completed successfully. and z = {optimal_value}"
        



