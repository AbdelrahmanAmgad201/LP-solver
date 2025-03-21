import numpy as np

def BigM(input):
    max_problem = input["max"]
    raw_tableau = input["model"]
    obj_fun = input["obj_fun"]
    
    headers = raw_tableau[0]  # Extract the column headers
    rows = raw_tableau[1:]  # Extract the numerical rows
    
    var_names = headers[1:-1]  # Exclude row names and 'sol'
    m = len(rows)  # Number of constraints
    n = len(var_names)  # Number of variables excluding 'sol'
    M = 1e6
    
    A = np.array([row[1:-1] for row in rows], dtype=float)  # Extract coefficients
    B = np.array([row[-1] for row in rows], dtype=float)  # Extract solution column
    basic_vars = [row[0] for row in rows]  # Identify basic variables (row names)
    
    # Identify artificial variables from row names
    artificial_vars = [i for i, var in enumerate(basic_vars) if var.startswith("a")]
    artificial_cal = [i for i, var in enumerate(headers) if var.startswith("a")]
    

    C_ext = np.zeros(A.shape[1])
    
    # Assign coefficients from obj_fun
    for i in range(len(obj_fun)):
        C_ext[i] = obj_fun[i]
    
    # Assign penalty to artificial variables
    for i, var in enumerate(var_names):
        if var.startswith("a"):
            C_ext[i] = -M if max_problem else M  # Artificial variable
    
    if  not max_problem:
        C_ext = -C_ext
    
    tableau = np.zeros((m + 1, A.shape[1] + 1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = B
    tableau[-1, :-1] = C_ext
    
    
    # Apply Big-M penalty to artificial variables
    for i in artificial_vars:
        tableau[-1] -= M * tableau[i] if max_problem else -M * tableau[i]
    
    cache = []
    steps = []
    
    basic_vars.append("z")
    while True:
        
        cache.append([headers] + [ [basic_vars[i]]+list(tableau[i]) for i in range(len(tableau))])
        if np.all(tableau[-1, :-1] >= 0 if max_problem else tableau[-1, :-1] <= 0):
            break

        entering = np.argmin(tableau[-1, :-1]) if max_problem else np.argmax(tableau[-1, :-1])
        valid_rows = tableau[:-1, entering] > 0
        ratios = np.full_like(tableau[:-1, -1], np.inf, dtype=float)
        ratios[valid_rows] = tableau[:-1, -1][valid_rows] / tableau[:-1, entering][valid_rows]
        
        if np.all(ratios == np.inf):
            print("The problem is unbounded.")
            return [], [], None, False, None
        
        leaving = np.argmin(ratios)
        steps.append(f"Pivot on row {leaving}, column {entering}")
        basic_vars[leaving] = headers[entering+1]
        pivot_element = tableau[leaving, entering]
        tableau[leaving] /= pivot_element
        for i in range(m + 1):
            if i != leaving:
                tableau[i] -= tableau[i, entering] * tableau[leaving]
    
    solution = np.zeros(A.shape[1])
    for i in range(m):
        if basic_vars[i] in headers:
            solution[headers.index(basic_vars[i]) - 1] = tableau[i, -1]
    
    if any(var in artificial_cal for var in range(m)):
        print("The problem is infeasible. Artificial variables remain in the basis.")
        return [], [], None, False, None  

    optimal_value = tableau[-1, -1] if max_problem else tableau[-1, -1]
    
    return steps, cache, [[solution[:n]]+[headers[1:-1]]], np.all(tableau[-1, :-1] >= 0 if max_problem else tableau[-1, :-1] <= 0), optimal_value


