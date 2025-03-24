from engines.simplex import Simplex
from resources.tableauBuilder import TableauBuilder
from methods.twoPhaseMethod import TwoPhaseMethod
import copy

class GoalProgrammingMethod:
    @staticmethod
    def solve(solver_input):
        steps = []
        tableaus = []

        tableau = TableauBuilder.build_goal_programming_tableau(solver_input)
        objectives = TableauBuilder.build_goal_objectives(tableau, solver_input)
        steps.append("creating tableau")
        tableaus.append(GoalProgrammingMethod.combine_tableau_objective(tableau, objectives))

        Simplex.make_consistent(tableau, objectives)
        steps.append("Making tableau consistent")
        tableaus.append(GoalProgrammingMethod.combine_tableau_objective(tableau, objectives))

        msg = None
        while (msg == None):
            msg, step = Simplex.iterate_once(tableau, objectives)
            steps.append(step)
            tableaus.append(GoalProgrammingMethod.combine_tableau_objective(tableau, objectives))

        return steps, tableaus, [Simplex.get_solution(tableaus[-1])], msg
    
    @staticmethod
    def combine_tableau_objective(tableau, zs):
        return copy.deepcopy(tableau[:1]) + copy.deepcopy(zs) + copy.deepcopy(tableau[1:])