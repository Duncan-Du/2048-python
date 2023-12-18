import math

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


log_dict = dict()


def smart_logs(n):
    if n in log_dict:
        return log_dict[n]
    else:
        log_dict[n] = math.log(n)
        return log_dict[n]


def log_smoothness_function(state: TwentyFortyEight.State):
    value = 0
    grid = state.game_matrix
    for i in range(4):
        for j in range(3):
            if grid[i][j] != 0 and grid[i][j] == grid[i][j + 1]:
                value += smart_logs(grid[i][j])

    for j in range(4):
        for i in range(3):
            if grid[i][j] != 0 and grid[i][j] == grid[i + 1][j]:
                value += smart_logs(grid[i][j])

    return value


def score_smoothness_function(state: TwentyFortyEight.State):
    return score_function(state) + 0.5 * smoothness_function(state)


def empty_tiles_and_max_tile(state: TwentyFortyEight.State):
    max_tile_value = 0
    empty_tile_count = 0
    for i in range(4):
        for j in range(4):
            if state.game_matrix[i][j] == 0:
                empty_tile_count += 1
            else:
                max_tile_value = max(max_tile_value, state.game_matrix[i][j])
    return empty_tile_count, max_tile_value


def empty_corners(state: TwentyFortyEight.State):
    count = 0
    grid = state.game_matrix
    if grid[0][0] == 0:
        count += 1
    if grid[0][3] == 0:
        count += 1
    if grid[3][0] == 0:
        count += 1
    if grid[3][3] == 0:
        count += 1
    return count


def exponential_decay(epsilon, decay_rate):
    """
    Performs exponential decay on epsilon and returns the new epsilon
    DECLAIMER: the below code (lines 28-34, not including any comments) were written by Bing Chat (Balanced)
    on 11/14/2023 with the prompt "Write a short piece of python code that performs the exponential decay for epsilon."
    """
    return epsilon * decay_rate


def step_decay(learning_rate, decay_rate, epoch, drop_every=5):
    """
    Performs step decay on learning_rate and returns the new learning_rate
    DECLAIMER: the below code (lines 37 and 45, not including any comments) were written by Bing Chat (Balanced)
    on 11/14/2023 with the prompt "Write a short piece of python code that performs the step decay for the
    learning rate."
    """
    if epoch > 1 and epoch % drop_every == 0:
        return learning_rate * decay_rate
    else:
        return learning_rate
