from project1.src.Problem import *
import queue
import copy


def read_from_console():
    print("Enter the numbers: ")
    puzzle = []
    position = []
    for i in range(0, 3):
        puzzle.append(input().split())
    for j in range(0, 3):
        for k in range(0, 3):
            if puzzle[j][k] == '0':
                position.append(j)
                position.append(k)
                puzzle = map(tuple, puzzle)
                puzzle = tuple(puzzle)
                position = tuple(position)
                return puzzle, position


def two_d_array_to_string(two_d_array):
    rows = len(two_d_array)
    cols = len(two_d_array[0])
    result = ""
    for i in range(0, rows):
        for j in range(0, cols):
            result += str(two_d_array[i][j])
    return result


class Action:
    def __init__(self, direction):  # up, down, right, left
        self.direction = direction


class State:
    def __init__(self, current_condition  # a tuple, showing the current condition of the puzzle
                 , position  # a tuple, showing the position of the zero
                 , path=None  # an array, showing the path to reach this state
                 , path_cost=0  # an integer, telling the cost we have payed till now
                 ):
        if path is None:
            path = []
        self.current_condition = current_condition
        self.path = path
        self.path_cost = path_cost
        self.position = position

    def expand(self):
        exp = queue.Queue()
        my_actions = DFS_graph.actions(self)
        for i in my_actions:
            result_state = DFS_graph.result(self, i)
            exp.put(State(current_condition=result_state.current_condition,
                          position=result_state.position,
                          path=self.path + [i.direction],
                          path_cost=self.path_cost + DFS_graph.action_cost(self, i)))
        return exp


class DFS_graph(Problem):
    puzzle, position = read_from_console()
    print(puzzle)

    def solve(self):
        lifo = queue.LifoQueue()
        e = set()
        root = self.initial_state()
        if self.goal_test(root):
            return
        lifo.put(root)
        e.add(two_d_array_to_string(root.current_condition))
        while not lifo.empty():
            current_state = lifo.get()
            if self.goal_test(current_state):
                self.print_path(current_state)
                return
            expanded = current_state.expand()
            while not expanded.empty():
                newly_generated = expanded.get()
                test = two_d_array_to_string(newly_generated.current_condition)
                if test not in e:
                    lifo.put(newly_generated)
                    e.add(test)
        print("Sorry! this puzzle is unsolvable :)")

    def print_path(self, state):
        path = state.path
        print("This is the path:", end=' ')
        for i in path:
            print(i, end=', ')
        print()
        print("This is the cost: " + str(state.path_cost))

    def goal_test(self, state):
        if state.current_condition == (('1','2','3'), ('4','5','6'), ('7','8','0')) or state.current_condition == (('0', '1', '2'), ('3', '4', '5'), ('6', '7', '8')):
            return True
        else:
            return False

    def initial_state(self):
        return State(DFS_graph.puzzle, DFS_graph.position)

    @staticmethod
    def result(state, action):

        def up():
            current_condition[position[0]][position[1]] = current_condition[position[0] - 1][position[1]]
            current_condition[position[0] - 1][position[1]] = '0'
            cc = map(tuple, current_condition)
            cc = tuple(cc)
            position[0] -= 1
            p = tuple(position)
            return State(cc, p)

        def down():
            current_condition[position[0]][position[1]] = current_condition[position[0] + 1][position[1]]
            current_condition[position[0] + 1][position[1]] = '0'
            cc = map(tuple, current_condition)
            cc = tuple(cc)
            position[0] += 1
            p = tuple(position)
            return State(cc, p)

        def right():
            current_condition[position[0]][position[1]] = current_condition[position[0] ][position[1]+1]
            current_condition[position[0]][position[1]+1] = '0'
            cc = map(tuple, current_condition)
            cc = tuple(cc)
            position[1] += 1
            p = tuple(position)
            return State(cc, p)

        def left():
            current_condition[position[0]][position[1]] = current_condition[position[0]][position[1] - 1]
            current_condition[position[0]][position[1] - 1] = '0'
            cc = map(tuple, current_condition)
            cc = tuple(cc)
            position[1] -= 1
            p = tuple(position)
            return State(cc, p)

        direction = {'up': up,
                     'down': down,
                     'right': right,
                     'left': left
                     }
        current_condition = map(list, state.current_condition)
        current_condition = list(current_condition)
        position = list(state.position)
        return direction.get(action.direction)()

    @staticmethod
    def actions(state):
        my_actions = []
        if state.position[0] > 0:
            my_actions.append(Action("up"))
        if state.position[0] < 2:
            my_actions.append(Action("down"))
        if state.position[1] > 0:
            my_actions.append(Action("left"))
        if state.position[1] < 2:
            my_actions.append(Action("right"))
        return my_actions

    @staticmethod
    def action_cost(state, action):
        return 1


dfs_graph = DFS_graph()
dfs_graph.solve()
