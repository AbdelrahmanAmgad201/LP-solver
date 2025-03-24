class Simplex:
    EPSILON = 1e-15  # Tolerance for floating-point comparisons
    # zs is the array of objectives
    
    @staticmethod
    def check_unbounded(tableau, zs):
        for z in zs:
            for i in range(1, len(z)-1):
                if z[i] <= Simplex.EPSILON:
                    continue
                flag = True
                for j in range(1, len(tableau)):
                    if tableau[j][i] > Simplex.EPSILON:
                        flag = False
                        break
                if flag:
                    return True

    @staticmethod     
    def get_entering_var(zs):
        x = -1
        mx = Simplex.EPSILON
        dropped_cols = []
        for z in zs:
            for i in range(1, len(z)-1):
                if (i not in dropped_cols) and z[i] < -Simplex.EPSILON:
                    dropped_cols.append(i)

        for z in range(len(zs)):
            for i in range(1, len(zs[z])-1):
                if zs[z][i] > mx and (i not in dropped_cols):
                    mx = zs[z][i]
                    x = i
            if x != -1: return x

        return x

    @staticmethod
    def check_infeasible(tableau):
        for i in tableau:
            if isinstance(i[0], str) and i[0][0] == 'a':
                return True
        return False
    
    @staticmethod
    def get_leaving_var(tableau, idx):
        x = -1
        mn = float('inf')
        for i in range(1, len(tableau)):
            if tableau[i][idx] > Simplex.EPSILON:
                tmp = tableau[i][-1] / tableau[i][idx]
                if tmp < mn - Simplex.EPSILON:
                    mn = tmp
                    x = i
        return x
    
    @staticmethod
    def make_consistent(tableau, zs):
        for row in range(1, len(tableau)):
            col = -1
            for i in range(len(tableau[0])):
                if (tableau[0][i] == tableau[row][0]):
                    col = i
                    break
                
            pivot = tableau[row][col]
            for i in range(1, len(tableau[0])):
                tableau[row][i] /= pivot

            for z in range(len(zs)):
                m = zs[z][col] / tableau[row][col]
                for j in range(1, len(zs[z])):
                    zs[z][j] -= m * tableau[row][j]
        
            for i in range(1, len(tableau)):
                if i == row:
                    continue
                m = tableau[i][col] / tableau[row][col]
                for j in range(1, len(tableau[0])):
                    tableau[i][j] -= m * tableau[row][j]
        

    @staticmethod
    def iterate_once(tableau, zs):
        step = ""
        if Simplex.check_unbounded(tableau, zs):
            return "unbounded", step
        
        enter_var_idx = Simplex.get_entering_var(zs)
        if enter_var_idx == -1:
            if Simplex.check_infeasible(tableau):
                return "infeasible", step
            return "optimal", step
        
        leave_var_idx = Simplex.get_leaving_var(tableau, enter_var_idx)
        # this condition should result in true
        if leave_var_idx == -1:
            return "unbounded", step
        
        step = f'Entering variable: {tableau[0][enter_var_idx]}, Leaving variable: {tableau[leave_var_idx][0]}'
        tableau[leave_var_idx][0] = tableau[0][enter_var_idx]

        Simplex.make_consistent(tableau, zs)

        enter_var_idx = Simplex.get_entering_var(zs)
        msg = None
        if enter_var_idx == -1:
            if Simplex.check_infeasible(tableau):
                msg = "infeasible"
            msg = "optimal"
        return msg, step

    @staticmethod
    def get_solution(tableau):
        sol = [[], []]
        for i in range(1, len(tableau[0])):
            sol[0].append(tableau[0][i])
            sol[1].append(0)

        for i in range(1, len(tableau)):
            for search in range(len(sol[0])):
                if sol[0][search] == tableau[i][0]:
                    sol[1][search] = tableau[i][-1]
                    break

        return sol
