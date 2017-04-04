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
                 , depth=0
                 ):
        if path is None:
            path = [] + [current_city]
        self.current_city = current_city
        self.path = path
        self.path_cost = path_cost
        self.depth = depth

    def expand(self):
        exp = queue.LifoQueue()
        if self.depth == int(limit)-1:
            return exp
        my_actions = DFS_limited_One.actions(self)
        for i in my_actions:
            exp.put(State(current_city=i.destination,
                          path=self.path + [i.destination],
                          path_cost=DFS_limited_One.path_cost(self, DFS_limited_One.action_cost(self, i)),
                          depth=self.depth+1))
        return exp


class DFS_limited_One(Problem):
    cities, routes = read_file()
    print(cities)

    def __init__(self):
        self.start = input("Specify the starting city: ")
        self.end = input("Specify the ending city: ")

    def solve(self):
        lifo = queue.LifoQueue()
        root = self.initial_state()
        if self.goal_test(root):
            return
        lifo.put(root)
        while not lifo.empty():
            current_state = lifo.get()
            if self.goal_test(current_state):
                self.print_path(current_state)
                return
            expanded = current_state.expand()
            while not expanded.empty():
                lifo.put(expanded.get())
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
        current_city_index = DFS_limited_One.cities.index(state.current_city)
        current_row = DFS_limited_One.routes[current_city_index]
        current_index = 0
        for i in current_row:
            if int(i) > 0:
                my_actions.append(Action(DFS_limited_One.cities[current_index]))
            current_index += 1
        return my_actions

    @staticmethod
    def action_cost(state, action):
        current_city_index = DFS_limited_One.cities.index(state.current_city)
        destination_city_index = DFS_limited_One.cities.index(action.destination)
        return int(DFS_limited_One.routes[current_city_index][destination_city_index])

limit = input("Specify the limit for the depth: ")
bfs_tree = DFS_limited_One()
bfs_tree.solve()
