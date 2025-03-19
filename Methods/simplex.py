import numpy as np

def simplex(input):
    max_problem = input["max"]
    A, B, C = input["model"][:-1, :-1], input["model"][:-1, -1], input["model"][-1, :-1]
    signs = input["sign"]
    m, n = A.shape
    new_A = A.copy()
    identity_matrix = np.eye(m)

    for i in range(m):
        new_A = np.hstack((new_A, identity_matrix[:, [i]]))

    num_new_vars = new_A.shape[1] - n
    C_ext = np.hstack((C, np.zeros(num_new_vars)))

    if max_problem:
        C_ext = -C_ext

    tableau = np.zeros((m + 1, new_A.shape[1] + 1))
    tableau[:-1, :-1] = new_A
    tableau[:-1, -1] = B
    tableau[-1, :-1] = C_ext

    steps, cache, solution,tableau = simplex_solver(tableau=tableau,n=new_A.shape[1],m=m)
    return steps, cache, solution[:n], np.all(tableau[-1, :-1] >= 0), tableau[-1, -1] 



def simplex_solver(tableau,n,m):
    cache = []
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

    return steps, cache, solution,tableau
