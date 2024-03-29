from project1.src.Problem import *
import queue


def read_from_console():
    missionaries = input("Enter the number of the missionaries: ")
    cannibals = input("Enter the number of the cannibals: ")
    return int(missionaries), int(cannibals)


class Action:
    def __init__(self, missionaries, cannibals):
        self.missionaries = missionaries
        self.cannibals = cannibals


class State:
    def __init__(self, left_missionaries, left_cannibals, right_missionaries, right_cannibals  # some integers
                 , boat  # a boolean. true means that the boat is on the left side, and false means the opposite
                 , path_cost=0
                 , path=None
                 ):
        if path is None:
            path = []
        self.left_missionaries = left_missionaries
        self.left_cannibals = left_cannibals
        self.right_missionaries = right_missionaries
        self.right_cannibals = right_cannibals
        self.boat = boat
        self.path_cost = path_cost
        self.path = path

    def expand(self):
        exp = queue.Queue()
        my_actions = BFS.actions(self)
        for i in my_actions:
            exp.put(BFS.result(self, i))
        return exp


class BFS(Problem):
    missionaries, cannibals = read_from_console()

    def solve(self):
        fifo = queue.Queue()
        root = self.initial_state()
        if self.goal_test(root):
            return
        fifo.put(root)
        while not fifo.empty():
            current_state = fifo.get()
            expanded = current_state.expand()
            while not expanded.empty():
                newly_generated = expanded.get()
                if self.goal_test(newly_generated):
                    self.print_path(newly_generated)
                    return
                fifo.put(newly_generated)
        print("Sorry! there is no way :)")

    def print_path(self, state):
        path = state.path
        print("This is the path: ")
        for i in path:
            print(i)
        print("This is the cost:" + str(state.path_cost))

    def goal_test(self, state):
        if state.right_missionaries == self.missionaries and state.right_cannibals == self.cannibals:
            return True
        else:
            return False

    def initial_state(self):
        return State(self.missionaries, self.cannibals, 0, 0, True)

    @staticmethod
    def path_cost(state, step_cost):
        return state.path_cost + step_cost

    @staticmethod
    def result(state, action):
        if state.boat:
            return State(state.left_missionaries - action.missionaries, state.left_cannibals - action.cannibals,
                         state.right_missionaries + action.missionaries, state.right_cannibals + action.cannibals,
                         not state.boat,
                         BFS.path_cost(state, BFS.action_cost(state, action)),
                         state.path + [[action.missionaries, action.cannibals]])
        else:
            return State(state.left_missionaries + action.missionaries, state.left_cannibals + action.cannibals,
                         state.right_missionaries - action.missionaries, state.right_cannibals - action.cannibals,
                         not state.boat,
                         BFS.path_cost(state, BFS.action_cost(state, action)),
                         state.path + [[action.missionaries, action.cannibals]])

    @staticmethod
    def actions(state):
        my_actions = []

        if state.boat:
            for i in range(0, 3):  # missionaries
                for j in range(0, 3 - i):  # cannibals
                    if (i == 0 and j == 0) or (i > state.left_missionaries) or (j > state.left_cannibals):
                        continue
                    if (state.left_missionaries - i == 0 or (state.left_missionaries - i) >= (state.left_cannibals - j)) and (state.right_missionaries + i == 0 or (state.right_missionaries + i) >= (state.right_cannibals + j)):
                        my_actions.append(Action(i, j))
        else:
            for i in range(0, 3):  # missionaries
                for j in range(0, 3 - i):  # cannibals
                    if (i == 0 and j == 0) or (i > state.right_missionaries) or (j > state.right_cannibals):
                        continue
                    if (state.left_missionaries + i == 0 or (state.left_missionaries + i) >= (state.left_cannibals + j)) and (state.right_missionaries - i == 0 or (state.right_missionaries - i) >= (state.right_cannibals - j)):
                        my_actions.append(Action(i, j))
        return my_actions

    @staticmethod
    def action_cost(state, action):
        return 1


bfs = BFS()
bfs.solve()
