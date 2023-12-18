import random
import time
from multiprocessing import Pool

import run
from game import TwentyFortyEight
from q_learning_agent import ApproximateQAgent

NUM_TRIES = 10
NUM_TRAIN = 1000
TIME_LIMIT = 10.
NUM_SIMULATIONS = 100
TOP_K = 10


def random_sample(pool):
    return random.sample(pool, k=1)[0]


def evaluate_parameters(portfolio):
    scores = 0
    for i in range(NUM_TRIES):
        agent = ApproximateQAgent(epsilon=portfolio[0], epsilon_decay_rate=portfolio[1],
                                  alpha=portfolio[2], learning_decay_rate=portfolio[3], discount=portfolio[4],
                                  time_limit=TIME_LIMIT)
        total_score = 0
        for i in range(NUM_SIMULATIONS):
            total_score += run.play_game(TwentyFortyEight(), agent)[0]
        scores += total_score / NUM_SIMULATIONS

    avg_score = scores / NUM_TRIES
    return portfolio, avg_score


if __name__ == '__main__':
    epsilons = [0.5 + i * 0.05 for i in range(11)]
    discount_factors = [1 - 0.1 * i for i in range(1, 4)]
    epsilon_decay_rates = [1 - 0.1 ** i for i in range(3, 7)]
    learning_rates = [0.005 * i for i in range(1, 6)]
    learning_decay_rates = [1 - 0.1 ** i for i in range(3, 5)]
    discount_factors = [1 - 0.05 * i for i in range(2, 7)]

    print(
        f"total num parameters = {len(epsilon_decay_rates) * len(epsilons) * len(epsilon_decay_rates) * len(learning_decay_rates) * len(learning_rates) * len(discount_factors)}")

    best_score = -1
    best_parameters = None
    start_time = time.time()

    portfolios = [(random_sample(epsilons), random_sample(epsilon_decay_rates), random_sample(learning_rates),
                   random_sample(learning_decay_rates), random_sample(discount_factors))
                  for _ in range(NUM_TRAIN)]

    results = None
    with Pool() as pool:
        results = pool.map(evaluate_parameters, portfolios)

    for portfolio, score in results:
        if score > best_score:
            best_parameters = portfolio
            best_score = score

    print(f"Training complete after {time.time() - start_time}s")
    print(f"best_score = {best_score}, best_params: {best_parameters}")
    sorted_index = sorted(range(len(results)), key=lambda i: results[i][1], reverse=True)
    print(f"Top {TOP_K} parameters:")
    for i in range(TOP_K):
        portfolio, score = results[sorted_index[i]]
        print("Score = {:.5f}: {}".format(score, str(portfolio)))
