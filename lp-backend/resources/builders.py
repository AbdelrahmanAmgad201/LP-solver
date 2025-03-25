def feedback_message(tableau, solver_input):
    map = dict()
    msg = f", z = {tableau[1][-1]}, "

    for i in range(len(tableau)):
        map[tableau[i][0]] = tableau[i][-1]

    n = solver_input.num_variables
    step = 1 if solver_input.all_non_negative else 2

    msg += "("
    for i in range(1, n+1):
        msg += f"x{i}"
        if i != n:
            msg += f", "
    msg += ") = "

    msg += "("
    for i in range(1, n+1):
        if step == 2:
            x = map.get(f"x{i}+", 0) - map.get(f"x{i}-", 0)
        else:
            x = map.get(f"x{i}", 0)
        
        msg += f"{x}"
        if i != n:
            msg += ", "
    msg += ")"

    return msg

def feedback_message_goalProgramming(tableau, solver_input):
    msg = ", "
    map = dict()
    for i in range(len(tableau)):
        map[tableau[i][0]] = tableau[i][-1]

    for i in range(1, solver_input.num_goals+1):
        z = map.get(f"z{i}", 0)
        optimal_msg = "(optimal)" if map.get(f"z{i}", 0) == 0 else ""
        msg += f"z{i} = {z} " + optimal_msg + ", "

    n = solver_input.num_variables
    step = 1 if solver_input.all_non_negative else 2

    msg += "("
    for i in range(1, n+1):
        msg += f"x{i}"
        if i != n:
            msg += f", "
    msg += ") = "

    msg += "("
    for i in range(1, n+1):
        if step == 2:
            x = map.get(f"x{i}+", 0) - map.get(f"x{i}-", 0)
        else:
            x = map.get(f"x{i}", 0)
        
        msg += f"{x}"
        if i != n:
            msg += ", "
    msg += ")"

    return msg