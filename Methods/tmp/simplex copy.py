import numpy as np


def simplex_solver(tableau,n,m):

    # TODO 
    """cache = []
    steps = []

    while True:
        cache.append(tableau.copy())
        if np.all(tableau[-1, :-1] >= 0):
            break

        entering = np.argmin(tableau[-1, :-1])
        valid_rows = tableau[:-1, entering] > 0
        ratios = np.full_like(tableau[:-1, -1], np.inf, dtype=float)
        ratios[valid_rows] = tableau[:-1, -1][valid_rows] / tableau[:-1, entering][valid_rows]
        
        if np.all(ratios == np.inf):
            raise ValueError("The problem is unbounded.")
        
        leaving = np.argmin(ratios)
        steps.append(f"Pivot on row {leaving}, column {entering}")
        pivot_element = tableau[leaving, entering]
        tableau[leaving] /= pivot_element
        for i in range(m + 1):
            if i != leaving:
                tableau[i] -= tableau[i, entering] * tableau[leaving]

    solution = np.zeros(n)
    basic_vars = np.where((tableau[:-1, :-1] == 1) & (np.sum(tableau[:-1, :-1] == 0, axis=0) == m-1))[1]
    
    for i, var in enumerate(basic_vars):
        print
        if i < tableau.shape[0] - 1:
            solution[var] = tableau[i, -1]

    return steps, cache, solution,tableau"""
