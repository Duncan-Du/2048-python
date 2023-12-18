import statistics
import sys
import multiprocessing
import tqdm

import utils
from expectimax_agent import ExpectimaxAgent
from q_learning_agent import ApproximateQAgent
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from mcts_agent import MCTSAgent
from game import TwentyFortyEight
from run import play_game, AgentGameGrid
from puzzle import GameGrid


def approximate_q_learning_worker(_):
    return play_game(TwentyFortyEight(), ApproximateQAgent(time_limit = 10.))

def expectimax_worker(_):
    return play_game(TwentyFortyEight(), ExpectimaxAgent(search_depth=2, heuristic_function=utils.score_function))

def expectimax_with_smoothness_worker(_):
    return play_game(TwentyFortyEight(), ExpectimaxAgent(search_depth=2, heuristic_function=utils.score_smoothness_function))

def random_worker(_):
    return play_game(TwentyFortyEight(), RandomAgent())

def greedy_worker(_):
    return play_game(TwentyFortyEight(), GreedyAgent())

def mcts_worker(_):
    return play_game(TwentyFortyEight(), MCTSAgent())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("----------------------------------------------")
        print("Welcome to Duncan & Bhavya's 2048 playground!")
        print("----------------------------------------------")
        print("2048 is a single-player sliding block puzzle game designed by Italian web developer Gabriele Cirulli. The game's objective is to slide numbered tiles on a grid to combine them to create a tile with the number 2048. However, one can continue to play the game after reaching the goal, creating tiles with larger numbers.")
        print("")
        print("We implemented a few different algorithms to play this game, and evaluated their results over a 1000 games to find the best algorithm for 2048. For each algorithm, we calculated the average score achieved by the agent over the 1000 games and the average number of wins, i.e. games where the 2048 tile was created.")
        print("")
        print("----------------------------------------------")
        print("Results")
        print("----------------------------------------------")
        print("The following are the results for each algorithm:")
        print("")
        print("Random agent : ")
        print("Average score: 881.976, Standard Deviation: 478.5893178489875")
        print("Average wins: 0.0, Standard Deviation: 0.0")
        print("")
        print("Greedy agent : ")
        print("Average score: 2636.696, Standard Deviation: 1423.214108271128")
        print("Average wins: 0.0, Standard Deviation: 0.0")
        print("")
        print("Expectimax agent, with depth 2 : ")
        print("Average score: 4273.404, Standard Deviation: 2099.9888299393097")
        print("Average wins: 0.0, Standard Deviation: 0.0")
        print("")
        print("Expectimax agent, with depth 2 and with smoothness : ")
        print("Average score: 5003.896, Standard Deviation: 2383.664954602429")
        print("Average wins: 0.0, Standard Deviation: 0.0")
        print("")
        print("Expectimax agent, with depth 3 : ")
        print("Average score: 5804.992, Standard Deviation: 2753.2880174153306")
        print("Average wins: 0.0, Standard Deviation: 0.0")
        print("")
        print("Expectimax agent, with depth 3 and with smoothness : ")
        print("Average score: 5937.948, Standard Deviation: 2791.3943540345094")
        print("Average wins: 0.0, Standard Deviation: 0.0")
        print("")
        print("Monte Carlo Tree Search agent : ")
        print("Average score: 11096.644, Standard Deviation: 4874.374333430538")
        print("Average wins: 0.093, Standard Deviation: 0.290577761426155")
        print("")
        print("----------------------------------------------")
        print("How to run the testing script - ")
        print("----------------------------------------------")
        print("The following packages are required to run the evaluation/visualization - ")
        print("tqdm, tkinter")
        print("Evaluation : to evaluate an agent over a number of games, run the executable with the following arguments (num_games must be at least 2) -")
        print("./2048Playground [num_games] [random|greedy|expectimax|expectimax_smoothness|mcts]")
        print("example usage:")
        print("./2048Playground 1000 mcts")
        print("")
        print("Visualization : to visualize a game, run the executable with the following arguments -")
        print("./2048Playground vis [random|greedy|expectimax|expectimax_smoothness|mcts]")
        print("")
        print("Play : Try out the game yourself! Run the following, and use the arrows keys to move the tiles -")
        print("./2048Playground play")
        print("")

    else:
        if sys.argv[1] == "play":
            GameGrid()
        elif sys.argv[1] == "vis":
            agent_name = sys.argv[2]
            if agent_name == 'expectimax':
                agent = ExpectimaxAgent(search_depth=2, heuristic_function=utils.score_function)
            elif agent_name == 'expectimax_smoothness':
                agent = ExpectimaxAgent(search_depth=2, heuristic_function=utils.score_smoothness_function)
            elif agent_name == 'random':
                agent = RandomAgent()
            elif agent_name == 'greedy':
                agent = GreedyAgent()
            elif agent_name == 'mcts':
                agent = MCTSAgent()
            elif agent_name == 'q_learning':
                agent = ApproximateQAgent(time_limit = 10.)
            AgentGameGrid(agent)
        else:
            n = int(sys.argv[1])
            agent = 'random'
            if len(sys.argv) >= 3:
                agent = sys.argv[2]
            with multiprocessing.Pool() as pool:
                if agent == 'expectimax':
                    results = list(tqdm.tqdm(pool.imap_unordered(expectimax_worker, range(n)), total=n))
                elif agent == 'expectimax_smoothness':
                    results = list(tqdm.tqdm(pool.imap_unordered(expectimax_with_smoothness_worker, range(n)), total=n))
                elif agent == 'random':
                    results = list(tqdm.tqdm(pool.imap_unordered(random_worker, range(n)), total=n))
                elif agent == 'greedy':
                    results = list(tqdm.tqdm(pool.imap_unordered(greedy_worker, range(n)), total=n))
                elif agent == 'mcts':
                    results = list(tqdm.tqdm(pool.imap_unordered(mcts_worker, range(n)), total=n))
                elif agent == 'q_learning':
                    results = list(tqdm.tqdm(pool.imap_unordered(approximate_q_learning_worker, range(n)), total=n))

            scores, wins = list(zip(*results))
            average_score = sum(scores) / n
            stddev_score = statistics.stdev(scores)
            average_wins = sum(wins) / n
            stddev_wins = statistics.stdev(wins)

            print(f'Average score: {average_score}, Standard Deviation: {stddev_score}')
            print(f'Average wins: {average_wins}, Standard Deviation: {stddev_wins}')