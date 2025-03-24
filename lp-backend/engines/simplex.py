class Simplex:
    EPSILON = 1e-15  # Tolerance for floating-point comparisons

    @staticmethod
    def check_unbounded(tableau, z):
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
    def get_entering_var(z):
        x = -1
        mx = Simplex.EPSILON
        for i in range(1, len(z)-1):
            if z[i] > mx:
                mx = z[i]
                x = i
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
    def make_consistent(tableau, z):
        for row in range(1, len(tableau)):
            col = -1
            for i in range(len(tableau[0])):
                if (tableau[0][i] == tableau[row][0]):
                    col = i
                    break
                
            pivot = tableau[row][col]
            for i in range(1, len(tableau[0])):
                tableau[row][i] /= pivot

            m = z[col] / tableau[row][col]
            for j in range(1, len(z)):
                z[j] -= m * tableau[row][j]
        
            for i in range(1, len(tableau)):
                if i == row:
                    continue
                m = tableau[i][col] / tableau[row][col]
                for j in range(1, len(tableau[0])):
                    tableau[i][j] -= m * tableau[row][j]
        

    @staticmethod
    def iterate_once(tableau, z):
        if Simplex.check_unbounded(tableau, z):
            return "unbounded"
        
        enter_var_idx = Simplex.get_entering_var(z)
        if enter_var_idx == -1:
            if Simplex.check_infeasible(tableau):
                return "infeasible"
            return "optimal"
        
        leave_var_idx = Simplex.get_leaving_var(tableau, enter_var_idx)
        # this condition should result in true
        if leave_var_idx == -1:
            return "unbounded"
        
        tableau[leave_var_idx][0] = tableau[0][enter_var_idx]

        Simplex.make_consistent(tableau, z)

        enter_var_idx = Simplex.get_entering_var(z)
        if enter_var_idx == -1:
            if Simplex.check_infeasible(tableau):
                return "infeasible"
            return "optimal"
        return None
