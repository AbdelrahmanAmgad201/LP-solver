from engines.simplex import Simplex
from resources.builders import feedback_message
from resources.tableauBuilder import TableauBuilder

class SimpleSimplex:
    @staticmethod
    def solve(tableau, solver_input):
        steps = []
        tableaus = []
        msg = None

        if Simplex.detect_artificial_variable(tableau):
            msg = "can't be solved with simple simplex algorithm"
            return steps, tableaus, [[[],[]]], msg

        zs = [TableauBuilder.build_objective(tableau, solver_input)]

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

        type_msg = "Simple Simplex (" + solver_input.optimization + "): "
        return steps, tableaus, [Simplex.get_solution(tableau)], type_msg + msg