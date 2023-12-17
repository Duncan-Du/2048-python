from game import State
from game import TwentyFortyEight


def score_function(state: State):
    return state.get_score()


def smoothness_function(state: TwentyFortyEight.State):
    value = 0
    grid = state.game_matrix
    for i in range(4):
        for j in range(3):
            if grid[i][j] != 0 and grid[i][j] == grid[i][j + 1]:
                value += grid[i][j]

    for j in range(4):
        for i in range(3):
            if grid[i][j] != 0 and grid[i][j] == grid[i + 1][j]:
                value += grid[i][j]

    # if value > 16:
    #     print(f"State {str(state)} has smoothness {value}")
    return value


def score_smoothness_function(state: TwentyFortyEight.State):
    return score_function(state) + 0.5 * smoothness_function(state)
