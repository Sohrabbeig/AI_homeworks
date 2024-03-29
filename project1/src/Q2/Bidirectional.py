from project1.src.Problem import *
import queue


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
        my_actions = Bidirectional.actions(self)
        for i in my_actions:
            result_state = Bidirectional.result(self, i)
            exp.put(State(current_condition=result_state.current_condition,
                          position=result_state.position,
                          path=self.path + [i.direction],
                          path_cost=self.path_cost + Bidirectional.action_cost(self, i)))
        return exp


class Bidirectional(Problem):
    puzzle, position = read_from_console()
    print(puzzle)

    def solve(self):
        queue1 = queue.Queue()
        queue2 = queue.Queue()
        e1 = set()
        e2 = set()
        start, end = self.initial_state()
        e1.add(two_d_array_to_string(start.current_condition))
        e2.add(two_d_array_to_string(end.current_condition))
        if self.goal_test(e1, e2):
            return
        queue1.put(start)
        queue2.put(end)
        while not queue1.empty() or not queue2.empty():
            if not queue1.empty():
                from_start = queue1.get()
                expanded1 = from_start.expand()
                while not expanded1.empty():
                    newly_generated1 = expanded1.get()
                    queue1.put(newly_generated1)
                    e1.add(two_d_array_to_string(newly_generated1.current_condition))
            if not queue2.empty():
                from_end = queue2.get()
                expanded2 = from_end.expand()
                while not expanded2.empty():
                    newly_generated2 = expanded2.get()
                    queue2.put(newly_generated2)
                    e2.add(two_d_array_to_string(newly_generated2.current_condition))
            if self.goal_test(e1, e2):
                common = e1.intersection(e2).pop()
                s1 = State
                s2 = State
                while True:
                    s1 = queue1.get()
                    k1 = two_d_array_to_string(s1.current_condition)
                    if common == k1:
                        break
                while True:
                    s2 = queue2.get()
                    k2 = two_d_array_to_string(s2.current_condition)
                    if common == k2:
                        break
                        print("salam")
                self.print_path(s1, s2)
        print("Sorry! there is no way :)")

    def print_path(self, s1, s2):
        path1 = s1.path
        path2 = s2.path
        print("This is the path:", end=' ')
        for i in path1:
            print(i, end=', ')
        for j in reversed(path2):
            print(i, end=', ')

        print("This is the cost: " + str(s1.path_cost + s2.path_cost))

    def goal_test(self, s1, s2):
        if len(s1.intersection(s2)) == 0:
            return False
        else:
            return True

    def initial_state(self):
        return State(Bidirectional.puzzle, Bidirectional.position), State((('1', '2', '3'), ('4', '5', '6'), ('7', '8', '0')), (2, 2))

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
            current_condition[position[0]][position[1]] = current_condition[position[0]][position[1] + 1]
            current_condition[position[0]][position[1] + 1] = '0'
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

Bidirectional = Bidirectional()
Bidirectional.solve()
