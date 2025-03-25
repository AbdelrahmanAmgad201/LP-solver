from engines.simplex import Simplex
from resources.tableauBuilder import TableauBuilder
import copy
class TwoPhaseMethod:
    @staticmethod
    def solve(tableau, solver_input):
        msg, steps, tableaus = TwoPhaseMethod.phase_one(tableau)
        if msg == "optimal":
            z = TableauBuilder.build_objective(tableaus[-1], solver_input)
            tableau = tableaus[-1][0:1] + tableaus[-1][2:]
            msg, steps2, tableaus2 = TwoPhaseMethod.phase_two(tableau, z)
            steps += steps2
            tableaus += tableaus2
        return steps, tableaus, [Simplex.get_solution(tableaus[-1])], msg

    @staticmethod
    def create_r(tableau):
        r = []
        for i in tableau[0]:
            if i == '.':
                r.append('r')
            elif i[0] == 'a':
                r.append(-1)
            else:
                r.append(0)
        return r
    
    @staticmethod
    def make_consistent(tableau, r):
        for i in range(len(tableau)):
            if (tableau[i][0][0] == 'a'):
                for j in range(1, len(tableau[i])):
                    r[j] += tableau[i][j]

    @staticmethod
    def phase_one(tableau):
        steps = []
        tableaus = []

        # create r = sum of artifitial variables
        r = [TwoPhaseMethod.create_r(tableau)]
        steps.append("Phase 1: creating tableau")
        tableaus.append(TwoPhaseMethod.combine_tableau_objective(tableau, r))

        Simplex.make_consistent(tableau, r)
        steps.append("making tableau consistent")
        tableaus.append(TwoPhaseMethod.combine_tableau_objective(tableau, r))

        msg = None
        while (msg == None):
            msg, step = Simplex.iterate_once(tableau, r)
            steps.append(step)
            tableaus.append(TwoPhaseMethod.combine_tableau_objective(tableau, r))

        if msg == "optimal":
            # remove artificial variable columns
            remove_indices = [i for i, col in enumerate(tableau[0]) if isinstance(col, str) and col.startswith('a')]
            filtered_tableau = [[row[i] for i in range(len(row)) if i not in remove_indices] for row in tableau]
            filtered_r = [[row[i] for i in range(len(row)) if i not in remove_indices] for row in r]
            steps.append("removing artifitial variables")
            tableaus.append(TwoPhaseMethod.combine_tableau_objective(copy.deepcopy(filtered_tableau), filtered_r))

        return msg, steps, tableaus

    @staticmethod
    def phase_two(tableau, z):
        steps = []
        tableaus = []

        zs = [z]
        steps.append("phase 2: creating tableau")
        tableaus.append(TwoPhaseMethod.combine_tableau_objective(tableau, zs))

        Simplex.make_consistent(tableau, zs)
        steps.append("making tableau consistent")
        tableaus.append(TwoPhaseMethod.combine_tableau_objective(tableau, zs))

        msg = None
        while (msg == None):
            msg, step = Simplex.iterate_once(tableau, zs)
            steps.append(step)
            tableaus.append(TwoPhaseMethod.combine_tableau_objective(tableau, zs))

        return msg, steps, tableaus

    @staticmethod
    def combine_tableau_objective(tableau, zs):
        return copy.deepcopy(tableau[:1]) + copy.deepcopy(zs) + copy.deepcopy(tableau[1:])