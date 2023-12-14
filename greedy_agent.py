import random
from game import State
from agent import Agent

class GreedyAgent(Agent):

    def __init__(self):
        super(GreedyAgent, self).__init__()


    def get_action(self, state: State):
        """
            Returns the action with the highest expected score
        """
        actions = state.get_actions()
        best_action = actions[0]
        scores = [succ.get_score() for succ in state.get_successors(best_action)]
        best_score = sum(scores)/len(scores)
        for action in actions[1:]:
            scores = [succ.get_score() for succ in state.get_successors(action)]
            score = sum(scores)/len(scores)
            if score > best_score:
                best_action = action
                best_score = score
        return best_action