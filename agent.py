from abc import ABC, abstractmethod

from game import TwentyFortyEight, State


class Agent(ABC):
    def __init__(self):
        pass

    """
    An agent must define a getAction method.
    """
    @abstractmethod
    def get_action(self, state: State):
        """
        The Agent will receive a State and must return an action.
        """
        pass