import sys
import multiprocessing

from expectimax_agent import ExpectimaxAgent
from game import TwentyFortyEight
from run import play_game

def worker(_):
    return play_game(TwentyFortyEight(), ExpectimaxAgent(search_depth=3))

if __name__ == '__main__':
    n = int(sys.argv[1])

    with multiprocessing.Pool() as pool:
        results = pool.map(worker, range(n))

    print(sum(results) / n)