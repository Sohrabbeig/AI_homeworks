from project1.src.Problem import *
import queue


def read_file():  # an integer greater than 0 is the cost of the route
                            # 0 is the cost of moving from one city to itself
                            # and -1 is for cases where there is no immediate route
    fm = open("map.txt", "r")
    cities = fm.readline().rstrip('\n').split(', ')
    routes = []
    for i in range(0, cities.__len__()):
        routes.append(fm.readline().rstrip('\n').split(', '))
    fm.close()
    return cities, routes


class Action:
    def __init__(self, destination):
        self.destination = destination


class State:
    def __init__(self, current_city  # a string, the name of the current city
                 , path=None  # an array, showing the path to reach this state
                 , path_cost=0  # an integer, telling the cost we have payed till now
                 ):
        if path is None:
            path = [] + [current_city]
        self.current_city = current_city
        self.path = path
        self.path_cost = path_cost

    def expand(self):
        exp = queue.Queue()
        my_actions = BFS_Tree_One.actions(self)
        for i in my_actions:
            exp.put(State(current_city=i.destination,
                          path=self.path + [i.destination],
                          path_cost=BFS_Tree_One.path_cost(self, BFS_Tree_One.action_cost(self, i))))
        return exp


class BFS_Tree_One(Problem):
    cities, routes = read_file()
    print(cities)

    def __init__(self):
        self.start = input("Specify the starting city:")
        self.end = input("Specify the ending city:")

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
        print("This is the path:", end=' ')
        for i in path:
            if i == self.end:
                print(i)
            else:
                print(i, end=' --> ')
        print("This is the cost:" + str(state.path_cost))

    def goal_test(self, state):
        if state.current_city == self.end:
            return True
        else:
            return False

    def initial_state(self):
        return State(self.start)

    @staticmethod
    def path_cost(state, step_cost):
        return state.path_cost+step_cost

    @staticmethod
    def result(state, action):
        return action.destination

    @staticmethod
    def actions(state):
        my_actions = []
        current_city_index = BFS_Tree_One.cities.index(state.current_city)
        current_row = BFS_Tree_One.routes[current_city_index]
        current_index = 0
        for i in current_row:
            if int(i) > 0:
                my_actions.append(Action(BFS_Tree_One.cities[current_index]))
            current_index += 1
        return my_actions

    @staticmethod
    def action_cost(state, action):
        current_city_index = BFS_Tree_One.cities.index(state.current_city)
        destination_city_index = BFS_Tree_One.cities.index(action.destination)
        return int(BFS_Tree_One.routes[current_city_index][destination_city_index])

bfs_tree = BFS_Tree_One()
bfs_tree.solve()
