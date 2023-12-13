import math

from agent import Agent
from game import State


def score_function(state: State):
    return state.get_score()


class ExpectimaxAgent(Agent):

    def __init__(self, heuristic_function=score_function, search_depth=5):
        self.depth = search_depth
        self.heuristic = heuristic_function

    def get_action(self, state: State):
        """
            Returns the expectimax action using self.depth and self.heuristic

            All ghosts should be modeled as choosing uniformly at random from their
            legal moves.
            """

        def value(state, layers):
            if state.is_terminal() or layers == 0:
                return None, self.heuristic(state)

            actions = state.get_actions()
            best_action = actions[0]
            max_value = -math.inf
            for sub_action in actions:
                # expected value
                exp_value = 0
                successors = state.get_successors(sub_action)
                for successor in successors:
                    a, v = value(successor, layers - 1)
                    exp_value += v

                exp_value /= len(actions)
                if exp_value > max_value:
                    max_value = exp_value
                    best_action = sub_action

            return best_action, max_value

        best_move, best_move_value = value(state, self.depth)

        return best_move
