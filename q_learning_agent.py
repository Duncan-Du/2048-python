import math
import random
import time

import game
import utils
from agent import Agent
from game import State, TwentyFortyEight


def get_features(state: TwentyFortyEight.State, action):
    features = dict()
    features["bias"] = 1.0
    next_grid, merge_dropped, reward = game.take_action_on_matrix(state.game_matrix, action)
    next_state = TwentyFortyEight.State(next_grid, state.score + reward)

    features["reward"] = 0 if reward == 0 else utils.smart_logs(reward)
    features["smoothness"] = utils.log_smoothness_function(state)
    features["future_smoothness"] = utils.log_smoothness_function(next_state)
    features["smoothness_difference"] = features["future_smoothness"] - features["smoothness"]

    features["empty_corners"] = utils.empty_corners(state)
    features["future_empty_corners"] = utils.empty_corners(next_state)
    features["empty_corners_difference"] = features["future_empty_corners"] - features["empty_corners"]

    empty_tiles, max_tile = utils.empty_tiles_and_max_tile(state)
    future_empty_tiles, future_max_tile = utils.empty_tiles_and_max_tile(next_state)
    future_empty_tiles -= 1  # a new tile will appear
    features["empty_tiles"] = empty_tiles
    features["future_empty_tiles"] = future_empty_tiles
    features["empty_tiles_difference"] = future_empty_tiles - empty_tiles
    features["max_tile_value"] = utils.smart_logs(max_tile)
    features["future_max_tile_value"] = utils.smart_logs(future_max_tile)
    features["max_tile_value_difference"] = features["future_max_tile_value"] - features["max_tile_value"]

    # don't even bother with future tile values because this is sooo much better
    # for i in range(4):
    #     for j in range(4):
    #         features['future_grid_' + str(i) + str(j)] = next_grid[i][j]

    return features


class ApproximateQAgent(Agent):
    def __init__(self, epsilon=0.5, discount=0.85, alpha=0.01,
                 epsilon_decay_rate: float = 0.9999, learning_decay_rate: float = 0.9999,
                 time_limit=0):
        super().__init__()
        self.weights = dict()
        self.epsilon = epsilon
        self.discount = discount
        self.alpha = alpha
        self.time_limit = time_limit
        self.epsilon_decay_rate = epsilon_decay_rate
        self.learning_decay_rate = learning_decay_rate

        self.learn()

    def get_q_value(self, state: TwentyFortyEight.State, action: TwentyFortyEight.Action):
        feature_func = get_features(state, action)
        feature_list = [feature_func[f_i] * self.weights.get(f_i, 0) for f_i in feature_func]
        return sum(feature_list)

    def compute_action_from_q_values(self, state: State):
        """
          Computes the best action to take in a state. If there
          are no legal actions, which is the case at the terminal state,
          returns None.
        """
        actions = state.get_actions()
        max_value = - math.inf
        best_action = None
        for action in actions:
            value = self.get_q_value(state, action)
            if value > max_value:
                max_value = value
                best_action = action

        if best_action is None:
            print("No legal action")

        return best_action

    def compute_value_from_q_values(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions. If
          there are no legal actions, which is the case at the
          terminal state, return 0
        """
        actions = state.get_actions()
        if len(actions) == 0:
            return 0.0
        max_value = - math.inf
        for action in actions:
            value = self.get_q_value(state, action)
            max_value = max(value, max_value)

        return max_value

    def update(self, state: TwentyFortyEight.State, action: TwentyFortyEight.Action, next_state: State, reward):
        """
          Observe a state = action => nextState and reward transition.
          Updates Q value
        """
        feature_func = get_features(state, action)
        diff = reward + self.discount * self.compute_value_from_q_values(next_state) - self.get_q_value(state, action)
        if math.isnan(diff):
            print("DEBUG: diff is nan")
        for w in feature_func:
            # if not self.weights.get(w, 0) + self.alpha * diff * feature_func[w] > -math.inf:
            # print(f"DEBUG: -inf at weight {w}. Prev weight = {self.weights.get(w, 0)}, diff = {diff}, reward = {reward}")
            self.weights[w] = self.weights.get(w, 0) + self.alpha * diff * feature_func[w]
        # print(self.weights)

    def get_action_learning(self, state: TwentyFortyEight.State):
        """
        With probability 1 - epsilon, selects action with the highest reward.
        With probability epsilon, selects action uniformly randomly.
        :param state: state position
        :return: action to perform
        """
        if random.random() < self.epsilon:
            # select action randomly
            actions = state.get_actions()
            return random.choice(actions)
        else:
            # select best action
            return self.compute_action_from_q_values(state)

    def learn(self):
        start_time = time.time()
        epoch = 0
        while time.time() - start_time < self.time_limit:
            curr_game = TwentyFortyEight()
            curr_state = curr_game.get_current_state()

            while not curr_state.is_terminal():
                action = self.get_action_learning(curr_state)
                # new_state, outcomes = model.result(curr_state, action)
                curr_game.take_action(action)
                new_state = curr_game.get_current_state()
                reward = new_state.score - curr_state.score
                # transform reward to log space
                if reward > 0:
                    reward = utils.smart_logs(reward)
                # update reward
                self.update(curr_state, action, new_state, reward)

                # update parameters
                curr_state = new_state

                self.epsilon = utils.exponential_decay(self.epsilon, self.epsilon_decay_rate)
                self.alpha = utils.step_decay(self.alpha, self.learning_decay_rate, epoch)
                epoch += 1
                # if epoch % 1000 == 0:
                # print(f"epoch {epoch}: epsilon = {self.epsilon}, learning rate alpha = {self.alpha}, current score = {curr_state.get_score()}")

        # print("DEBUG: done learning")
        # print(self.weights)
        # after learning, set to 0
        self.epsilon = 0.0  # no exploration
        self.alpha = 0.0  # no learning

    def get_action(self, state: State):
        return self.compute_action_from_q_values(state)
