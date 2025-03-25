class TableauBuilder:
    @staticmethod
    def build_tableau(solver_input):
        tableau = []
        for i in range(solver_input.num_constraints + 1):
            tableau.append(['.'])
        
        if solver_input.all_non_negative:
            for i in range(solver_input.num_variables):
                tableau[0].append(f'x{i+1}')
                sign = 1
                if solver_input.constraints[i].rhs < 0:
                    sign = -1
                for j in range(solver_input.num_constraints):
                    tableau[j+1].append(solver_input.constraints[j].coefficients[i] * sign)
        else:
            for i in range(solver_input.num_variables):
                tableau[0].append(f'x{i+1}+')
                tableau[0].append(f'x{i+1}-')
                sign = 1
                if solver_input.constraints[i].rhs < 0:
                    sign = -1
                for j in range(solver_input.num_constraints):
                    tableau[j+1].append(solver_input.constraints[j].coefficients[i] * sign)
                    tableau[j+1].append(-solver_input.constraints[j].coefficients[i] * sign)
            
        for i in range(solver_input.num_constraints):
            operator = solver_input.constraints[i].operator
            if solver_input.constraints[i].rhs < 0:
                if operator == "<=":
                    operator = ">="
                elif operator == ">=":
                    operator = "<="

            if (operator == "<="):
                tableau[i+1][0] = f'u{i+1}'
                tableau[0].append(f'u{i+1}')
                for j in range(solver_input.num_constraints):
                    tableau[j+1].append(1 if i == j else 0)

            elif (operator == ">="):
                tableau[0].append(f'e{i+1}')
                for j in range(solver_input.num_constraints):
                    tableau[j+1].append(-1 if i == j else 0)

            if (operator == "=" or operator == ">="):
                tableau[i+1][0] = f'a{i+1}'
                tableau[0].append(f'a{i+1}')
                for j in range(solver_input.num_constraints):
                    tableau[j+1].append(1 if i == j else 0)

        tableau[0].append("sol")
        for i in range(solver_input.num_constraints):
            sign = 1
            if solver_input.constraints[i].rhs < 0:
                sign = -1
            tableau[i+1].append(solver_input.constraints[i].rhs * sign)


        return tableau
    
    @staticmethod
    def build_objective(tableau, solver_input):
        sign = (1 if solver_input.optimization == "minimize" else -1)
        obj_fun = ['z']
        for i in solver_input.objective.coefficients:
            # -1 to make all variables LHS and sign is to turn maximize problems into minimize
            obj_fun.append(i * -1 * sign)
            if not solver_input.all_non_negative:
                obj_fun.append(-i * -1 * sign)

        n = 1 if solver_input.all_non_negative else 2
        for i in range(len(solver_input.objective.coefficients * n)+1, len(tableau[0])):
            obj_fun.append(0)

        return obj_fun
    
    @staticmethod
    def build_goal_programming_tableau(solver_input):
        tableau = []
        for i in range(solver_input.num_goals + solver_input.num_constraints + 1):
            tableau.append(['.'])

        if solver_input.all_non_negative:
            for i in range(solver_input.num_variables):
                tableau[0].append(f'x{i+1}')
                for j in range(1, solver_input.num_goals+1):
                    tableau[j].append(solver_input.goals[j-1].coefficients[i])

                for j in range(solver_input.num_goals + 1, solver_input.num_goals + solver_input.num_constraints + 1):
                    tableau[j].append(solver_input.constraints[j - solver_input.num_goals - 1].coefficients[i])
        else:
            for i in range(solver_input.num_variables):
                tableau[0].append(f'x{i+1}+')
                tableau[0].append(f'x{i+1}-')
                for j in range(1, solver_input.num_goals+1):
                    tableau[j].append(solver_input.goals[j-1].coefficients[i])
                    tableau[j].append(-solver_input.goals[j-1].coefficients[i])

                for j in range(solver_input.num_goals + 1, solver_input.num_goals + solver_input.num_constraints + 1):
                    tableau[j].append(solver_input.constraints[j - solver_input.num_goals - 1].coefficients[i])
                    tableau[j].append(-solver_input.constraints[j - solver_input.num_goals - 1].coefficients[i])

        for i in range(solver_input.num_goals):
            tableau[0].append(f'u{i+1}')
            tableau[0].append(f'e{i+1}')
            for j in range(1, len(tableau)):
                if i+1 == j:
                    tableau[j][0] = f'u{i+1}'
                    tableau[j].append(1)
                    tableau[j].append(-1)
                else:
                    tableau[j].append(0)
                    tableau[j].append(0)

        for i in range(solver_input.num_constraints):
            operator = solver_input.constraints[i].operator
            if (operator == "<="):
                tableau[0].append(f'u{solver_input.num_goals + i + 1}')
                tableau[solver_input.num_goals + i + 1][0] = f'u{solver_input.num_goals + i + 1}'
                for j in range(1, len(tableau)):
                    tableau[j].append(1 if solver_input.num_goals + i + 1 == j else 0)

            elif (operator == ">="):
                tableau[0].append(f'e{solver_input.num_goals + i + 1}')
                for j in range(1, len(tableau)):
                    tableau[j].append(-1 if solver_input.num_goals + i + 1 == j else 0)

            if (operator == "=" or operator == ">="):
                tableau[0].append(f'a{solver_input.num_goals + i + 1}')
                tableau[solver_input.num_goals + i + 1][0] = f'a{solver_input.num_goals + i + 1}'
                for j in range(1, len(tableau)):
                    tableau[j].append(1 if solver_input.num_goals + i + 1 == j else 0)

        tableau[0].append("sol")
        i = 1
        for j in solver_input.goals:
            tableau[i].append(j.rhs)
            i += 1
        for j in solver_input.constraints:
            tableau[i].append(j.rhs)
            i += 1

        return tableau
    
    @staticmethod
    def build_goal_objectives(tableau, solver_input):
        objectives = []
        for i in range(solver_input.num_goals):
            z = [f'z{i+1}']
            for j in range(1, len(tableau[0])):
                op = solver_input.goals[i].operator
                var = tableau[0][j]
                z.append(-1 if ((op == ">=" or op == "=") and var == f'u{i+1}') or ((op == "<=" or op == "=") and var == f'e{i+1}') else 0)
            objectives.append(z)
        return objectives
                    

