import statistics
import sys
import multiprocessing
import tqdm

import utils
from expectimax_agent import ExpectimaxAgent
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from mcts_agent import MCTSAgent
from game import TwentyFortyEight
from run import play_game


def expectimax_worker(_):
    return play_game(TwentyFortyEight(), ExpectimaxAgent(search_depth=3, heuristic_function=utils.score_function))

def expectimax_with_smoothness_worker(_):
    return play_game(TwentyFortyEight(), ExpectimaxAgent(search_depth=3, heuristic_function=utils.score_smoothness_function))

def random_worker(_):
    return play_game(TwentyFortyEight(), RandomAgent())

def greedy_worker(_):
    return play_game(TwentyFortyEight(), GreedyAgent())

def mcts_worker(_):
    return play_game(TwentyFortyEight(), MCTSAgent())

if __name__ == '__main__':
    n = int(sys.argv[1])
    agent = 'random'
    if len(sys.argv) >= 3:
        agent = sys.argv[2]

    with multiprocessing.Pool() as pool:
        if agent == 'expectimax':
            results = list(tqdm.tqdm(pool.imap_unordered(expectimax_worker, range(n)), total=n))
        elif agent == 'random':
            results = list(tqdm.tqdm(pool.imap_unordered(random_worker, range(n)), total=n))
        elif agent == 'greedy':
            results = list(tqdm.tqdm(pool.imap_unordered(greedy_worker, range(n)), total=n))
        elif agent == 'mcts':
            results = list(tqdm.tqdm(pool.imap_unordered(mcts_worker, range(n)), total=n))

    scores, wins = list(zip(*results))
    average_score = sum(scores) / n
    stddev_score = statistics.stdev(scores)
    average_wins = sum(wins) / n
    stddev_wins = statistics.stdev(wins)

    print(f'Average score: {average_score}, Standard Deviation: {stddev_score}')
    print(f'Average wins: {average_wins}, Standard Deviation: {stddev_wins}')