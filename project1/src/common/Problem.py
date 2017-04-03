class State:
    pass


class Action:
    pass


class Problem:
    def initial_state(self):
        pass

    def actions(self, state):
        pass

    def result(self, state):
        pass

    def goal_test(self, state):
        pass

    def action_cost(self, state, action):
        pass

    def path_cost(self, path):
        pass
