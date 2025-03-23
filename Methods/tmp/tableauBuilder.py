class TableauBuilder:
    @staticmethod
    def build_tableau(solver_input):
        tableau = []
        for i in range(solver_input.num_constraints + 1):
            tableau.append(['.'])
        
        for i in range(solver_input.num_variables):
            tableau[0].append(f'x{i+1}')
            for j in range(solver_input.num_constraints):
                tableau[j+1].append(solver_input.constraints[j].coefficients[i])
            
        for i in range(solver_input.num_constraints):
            operator = solver_input.constraints[i].operator
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
            tableau[i+1].append(solver_input.constraints[i].rhs)

        return tableau
    
    @staticmethod
    def build_objective(tableau, solver_input):
        sign = (1 if solver_input.optimization == "minimize" else -1)
        obj_fun = ['z']
        for i in solver_input.objective.coefficients:
            # -1 to make all variables LHS and sign is to turn maximize problems into minimize
            obj_fun.append(i * -1 * sign)
        
        for i in range(len(solver_input.objective.coefficients)+1, len(tableau[0])):
            obj_fun.append(0)

        return obj_fun
    