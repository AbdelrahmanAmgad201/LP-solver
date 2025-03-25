from engines.simplex import Simplex
from resources.tableauBuilder import TableauBuilder
from resources.builders import feedback_message

class M_Method:
    @staticmethod
    def solve(tableau, solver_input):
        steps = []
        tableaus = []
        msg = None

        zs = [TableauBuilder.build_objective(tableau, solver_input)]
        M_Method.m_method_objective(tableau, zs)

        steps.append("creating tableau")
        tableaus.append(Simplex.combine_tableau_objective(tableau, zs))

        while (msg == None):
            msg, step = Simplex.iterate_once(tableau, zs)
            steps.append(step)
            tableaus.append(Simplex.combine_tableau_objective(tableau, zs))

        if solver_input.optimization == "maximize":
                Simplex.fix_z_sign(tableaus)
            
        if msg == "optimal":
             msg += feedback_message(tableaus[-1], solver_input)

        type_msg = "M Method (" + solver_input.optimization + "): "
        return steps, tableaus, [Simplex.get_solution(tableau)], type_msg + msg
    
    @staticmethod
    def m_method_objective(tableau, zs):
        m = max(zs[0][1:]) * 100
        for i in range(1, len(tableau)-1):
            if tableau[0][i][0] == 'a':
                zs[0][i] = m