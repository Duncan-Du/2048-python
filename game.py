import random
from abc import ABC, abstractmethod
from enum import Enum

import logic


class Game(ABC):
    """ A two-player zero-sum perfect information game.
    """

    @abstractmethod
    def initial_state(self):
        """ Returns the initial state of this game.
        """
        pass


class State(ABC):
    """ A state in a game.
    """

    @abstractmethod
    def is_terminal(self):
        """ Determines if this state is terminal.  Return value is true is so and false otherwise.

            self -- a state
        """
        pass

    def payoff(self):
        """ Returns the payoff for player 0 at this terminal state.

            self -- a terminal state
        """
        return 0.0  # default is a draw

    @abstractmethod
    def get_actions(self):
        """ Returns a list of possible actions in this nonterminal state.
            The representation of each state is left to the implementation.

            self -- a nonterminal state
        """
        pass

    def is_legal(self, action):
        """ Determines if the given action is legal in this state.

            self -- a state
            action -- an action
        """
        return False

    @abstractmethod
    def successor(self, action):
        """ Returns the state that results from the given action in this nonterminal state.

            self -- a nonterminal state
            action -- one of the actions in the list returned by get_actions for this state
        """
        pass


def generate_successors(mat):
    empty_cells = []
    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] == 0:
                empty_cells.append((i, j))

    assert len(empty_cells) > 0
    successors = []
    for i, j in empty_cells:
        next_mat = [row.copy() for row in mat]
        next_mat[i, j] = random.randint(1, 2) * 2
        successors.append(next_mat)

    return generate_successors(mat)


class TwentyFortyEight(Game):
    def __init__(self, n = 4):
        """
        Initializes a new 2048 game with an n-by-n grid.
        :param n: grid size
        """

    class Action(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    class State(State):

        def __init__(self, n=4):
            self.game_matrix = logic.new_game(n)
            self.score = 0


        def is_legal(self, action):
            if action == TwentyFortyEight.Action.UP:
                next_mat, success, reward = logic.up(self.game_matrix)
            elif action == TwentyFortyEight.Action.UP:
                next_mat, success, reward = logic.right(self.game_matrix)
            elif action == TwentyFortyEight.Action.DOWN:
                next_mat, success, reward = logic.down(self.game_matrix)
            elif action == TwentyFortyEight.Action.LEFT:
                next_mat, success, reward = logic.left(self.game_matrix)
            else:
                return False

            return success

        def is_terminal(self):
            game_state_result = logic.game_state(self.game_matrix)
            return game_state_result == 'win' or game_state_result == 'lose'


        def copy(self):
            new_state = State(n=len(self.game_matrix))
            new_state.game_matrix = [row.copy() for row in self.game_matrix]
            new_state.score = self.score
            return new_state

        def get_actions(self):
            pass
