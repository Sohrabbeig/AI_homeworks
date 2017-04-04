def read_file():
    pass


class Problem:

    def initial_state(self):
        pass

    @staticmethod
    def actions(state):
        pass

    @staticmethod
    def result(state, action):
        pass

    def goal_test(self, state):
        pass

    @staticmethod
    def action_cost(state, action):
        pass

    @staticmethod
    def path_cost(state, step_cost):
        pass

    def solve(self):
        pass

