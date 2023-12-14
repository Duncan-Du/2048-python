import random
from game import State
from agent import Agent

class RandomAgent(Agent):

    def __init__(self):
        super(RandomAgent, self).__init__()


    def get_action(self, state: State):
        """
            Returns a random action from the list of legal actions
        """
        actions = state.get_actions()
        return random.choice(actions)