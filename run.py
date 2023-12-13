from agent import Agent
from expectimax_agent import ExpectimaxAgent
from game import TwentyFortyEight


def play_game(game: TwentyFortyEight, agent: Agent):
    while not game.get_current_state().is_terminal():
        next_action = agent.get_action(game.get_current_state())
        game.take_action(next_action)

    return game.get_current_state().score



if __name__ == '__main__':
    expecti_agent = ExpectimaxAgent(search_depth=2)
    print(play_game(TwentyFortyEight(), expecti_agent))