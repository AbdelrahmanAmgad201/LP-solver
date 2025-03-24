from engines.simplex import Simplex
class TwoPhaseMethod:
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
        # create r = sum of artifitial variables
        r = TwoPhaseMethod.create_r(tableau)
        Simplex.make_consistent(tableau, r)
        print("---- Phase One ----")
        i = 1
        while (True):
            print(f"step {i}:")
            msg = Simplex.iterate_once(tableau, r)
            for t in tableau:
                print(t)
            print(r)
            print("--------")
            if msg != None:
                break
            i += 1

        if msg == "optimal":
            # remove artificial variable columns
            remove_indices = [i for i, col in enumerate(tableau[0]) if isinstance(col, str) and col.startswith('a')]
            filtered_tableau = [[row[i] for i in range(len(row)) if i not in remove_indices] for row in tableau]
            for t in filtered_tableau:
                print(t)
            print("reached intial fiseable solution")
            return msg, filtered_tableau
        print(msg)
        return msg, None


    @staticmethod
    def phase_two(tableau, z):
        print("---- Phase Two ----")
        Simplex.make_consistent(tableau, z)
        for t in tableau:
            print(t)
        print(z)
        print("-----")
        i = 1
        while (True):
            print(f"step {i}:")
            msg = Simplex.iterate_once(tableau, z)
            for t in tableau:
                print(t)
            print(z)
            print("--------")
            if msg != None:
                break
            i += 1
        print(msg)

