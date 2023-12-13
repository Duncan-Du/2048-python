import random
from abc import ABC, abstractmethod
from enum import Enum

import logic


class Game(ABC):
    """ A two-player zero-sum perfect information game.
    """

    @abstractmethod
    def get_current_state(self):
        """ Returns the current state of this game.
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

    @abstractmethod
    def get_score(self):
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

    @abstractmethod
    def is_legal(self, action):
        """ Determines if the given action is legal in this state.

            self -- a state
            action -- an action
        """
        return False

    @abstractmethod
    def get_successors(self, action):
        """ Returns the states that could result from the given action in this nonterminal state in a list.

            self -- a nonterminal state
            action -- one of the actions in the list returned by get_actions for this state
        """
        pass


def take_action_on_matrix(matrix, action):
    if action == TwentyFortyEight.Action.UP:
        next_mat, success, reward = logic.up(matrix)
    elif action == TwentyFortyEight.Action.RIGHT:
        next_mat, success, reward = logic.right(matrix)
    elif action == TwentyFortyEight.Action.DOWN:
        next_mat, success, reward = logic.down(matrix)
    elif action == TwentyFortyEight.Action.LEFT:
        next_mat, success, reward = logic.left(matrix)
    else:
        print("Unexpected action")
        return False

    return next_mat, success, reward


class TwentyFortyEight(Game):
    def __init__(self):
        """
        Initializes a new 2048 game with an n-by-n grid.
        :param n: grid size
        """
        self.game_state = TwentyFortyEight.State(logic.new_game(4), score=0)

    def take_action(self, action):
        assert self.game_state.is_legal(action)
        next_state = random.choices(self.game_state.get_successors(action), k = 1)[0]
        self.game_state = next_state

    def get_current_state(self):
        return self.game_state

    class Action(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

    class State(State):

        def __init__(self, matrix=None, score=0):
            self.game_matrix = matrix
            self.score = score
            self.successors = dict()

        def is_legal(self, action):
            if action == TwentyFortyEight.Action.UP:
                next_mat, success, reward = logic.up(self.game_matrix)
            elif action == TwentyFortyEight.Action.RIGHT:
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
            new_state = State()
            new_state.game_matrix = [row.copy() for row in self.game_matrix]
            new_state.score = self.score
            return new_state

        def get_actions(self):
            legal_actions = []
            for action in list(TwentyFortyEight.Action):
                if self.is_legal(action):
                    legal_actions.append(action)
            return legal_actions

        def get_successors(self, action):
            def generate_new_tile(mat):
                empty_cells = []
                for i in range(len(mat)):
                    for j in range(len(mat)):
                        if mat[i][j] == 0:
                            empty_cells.append((i, j))

                assert len(empty_cells) > 0
                successors = []
                for i, j in empty_cells:
                    next_mat = [row.copy() for row in mat]
                    next_mat[i][j] = random.randint(1, 2) * 2
                    successors.append(next_mat)

                return successors

            assert self.is_legal(action)

            if action in self.successors:
                return self.successors[action]

            next_matrix, done, reward = take_action_on_matrix(self.game_matrix, action)
            possible_successor_matrices = generate_new_tile(next_matrix)
            successors = []
            for new_matrix in possible_successor_matrices:
                new_state = TwentyFortyEight.State(new_matrix, score=self.score + reward)
                successors.append(new_state)

            # memorize successors for future
            self.successors[action] = successors
            return successors

        def get_score(self):
            return self.score
