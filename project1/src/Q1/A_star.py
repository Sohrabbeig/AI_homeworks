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
    fh = open("heuristic.txt", "r")
    h = fh.readline().rstrip('\n').split(', ')
    fh.close()
    return cities, routes, h


class Action:
    def __init__(self, destination):
        self.destination = destination


class State:
    def __init__(self, current_city  # a string, the name of the current city
                 , estimated
                 , path=None  # an array, showing the path to reach this state
                 , path_cost=0  # an integer, telling the cost we have payed till now
                 ):
        if path is None:
            path = [] + [current_city]
        self.current_city = current_city
        self.path = path
        self.path_cost = path_cost
        self.estimated = estimated

    def expand(self):
        exp = queue.LifoQueue()
        my_actions = A_star.actions(self)
        for i in my_actions:
            exp.put(State(current_city=i.destination,
                          estimated=A_star.h_function(i.destination),
                          path=self.path + [i.destination],
                          path_cost=A_star.path_cost(self, A_star.action_cost(self, i))))
        return exp

    def __lt__(self, other):
        if self.path_cost+self.estimated < other.path_cost+other.estimated:
            return True
        else:
            return False


class A_star(Problem):
    cities, routes, h = read_file()
    print(cities)

    def __init__(self):
        self.start = input("Specify the starting city: ")
        self.end = input("Specify the ending city: ")

    def h_function(self, destination):
        return int(A_star.h[A_star.cities.index(destination)])

    def solve(self):
        p_queue = queue.PriorityQueue()
        root = self.initial_state()
        if self.goal_test(root):
            return
        p_queue.put(root)
        while not p_queue.empty():
            current_state = p_queue.get()
            if self.goal_test(current_state):
                self.print_path(current_state)
                return
            expanded = current_state.expand()
            while not expanded.empty():
                new = expanded.get()
                p_queue.put(new)
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
        return State(self.start, int(A_star.h[A_star.cities.index(self.start)]))

    @staticmethod
    def path_cost(state, step_cost):
        return state.path_cost+step_cost

    @staticmethod
    def result(state, action):
        return action.destination

    @staticmethod
    def actions(state):
        my_actions = []
        current_city_index = A_star.cities.index(state.current_city)
        current_row = A_star.routes[current_city_index]
        current_index = 0
        for i in current_row:
            if int(i) > 0:
                my_actions.append(Action(A_star.cities[current_index]))
            current_index += 1
        return my_actions

    @staticmethod
    def action_cost(state, action):
        current_city_index = A_star.cities.index(state.current_city)
        destination_city_index = A_star.cities.index(action.destination)
        return int(A_star.routes[current_city_index][destination_city_index])

A_star = A_star()
A_star.solve()
