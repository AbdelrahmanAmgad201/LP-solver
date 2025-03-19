import numpy as np

def BigM(input):
    max_problem = input["max"]
    A, B, C = input["model"][:-1, :-1], input["model"][:-1, -1], input["model"][-1, :-1]
    signs = input["sign"]
    m, n = A.shape
    M = 1e6

    artificial_vars = []
    new_A = A.copy()
    identity_matrix = np.eye(m)

    for i in range(m):
        if signs[i] == "<=":
            new_A = np.hstack((new_A, identity_matrix[:, [i]]))
        elif signs[i] == ">=":
            surplus_col = -identity_matrix[:, [i]]
            artificial_col = identity_matrix[:, [i]]
            new_A = np.hstack((new_A, surplus_col, artificial_col))
            artificial_vars.append(new_A.shape[1] - 1)
        elif signs[i] == "=":
            artificial_col = identity_matrix[:, [i]]
            new_A = np.hstack((new_A, artificial_col))
            artificial_vars.append(new_A.shape[1] - 1)

    num_new_vars = new_A.shape[1] - n
    C_ext = np.hstack((C, np.zeros(num_new_vars)))

    for idx in artificial_vars:
        C_ext[idx] = M if not max_problem else -M

    if max_problem:
        C_ext = -C_ext

    tableau = np.zeros((m + 1, new_A.shape[1] + 1))
    tableau[:-1, :-1] = new_A
    tableau[:-1, -1] = B
    tableau[-1, :-1] = C_ext

    
    for i, idx in enumerate(artificial_vars):
        row_index = np.where(tableau[:, idx] == 1)[0]  # Get row indices where column `idx` has 1
        if len(row_index) > 0:
            row_index = row_index[0]  # Take the first row index
            tableau[-1] -= M * tableau[row_index]
        

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

    solution = np.zeros(new_A.shape[1])
    basic_vars = np.where((tableau[:-1, :-1] == 1) & (np.sum(tableau[:-1, :-1] == 0, axis=0) == m-1))[1]
    
    for i, var in enumerate(basic_vars):
        if i < tableau.shape[0] - 1:
            solution[var] = tableau[i, -1]

    
    if any(var in artificial_vars for var in basic_vars):
        return None, None, None, False, None  
 

    optimal_value = tableau[-1, -1] 
    return steps, cache, solution[:n], np.all(tableau[-1, :-1] >= 0), optimal_value
