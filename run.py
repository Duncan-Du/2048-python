import sys
from time import sleep

from agent import Agent
from expectimax_agent import ExpectimaxAgent
from q_learning_agent import ApproximateQAgent
from random_agent import RandomAgent
from greedy_agent import GreedyAgent
from mcts_agent import MCTSAgent
from game import TwentyFortyEight
import constants as c
from tkinter import Frame, Label, CENTER
import logic


def play_game(game: TwentyFortyEight, agent: Agent):
    while not game.get_current_state().is_terminal():
        next_action = agent.get_action(game.get_current_state())
        game.take_action(next_action)
    # if game.get_current_state().has_2048():
    #     print("Reached 2048!")
    return game.get_current_state().score, int(game.get_current_state().has_2048())

class AgentGameGrid(Frame):
    def __init__(self, agent):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')


        self.grid_cells = []
        self.init_grid()
        self.game = TwentyFortyEight()
        self.agent = agent
        self.history_matrixs = []
        self.update_grid_cells()

        self.play()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=3)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.game.game_state.game_matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def play(self, sleep_time = 0.1):
        while not self.game.get_current_state().is_terminal():
            next_action = self.agent.get_action(self.game.get_current_state())
            self.game.take_action(next_action)
            self.update_grid_cells()
            sleep(sleep_time)
        # if self.game.get_current_state().has_2048():
        #     print("Reached 2048!")
        print(self.game.get_current_state().score)


if __name__ == '__main__':
    # expecti_agent = ExpectimaxAgent(search_depth=5)
    # if len(sys.argv) <= 1:
    #     print(play_game(TwentyFortyEight()[0], expecti_agent))
    # else:
    #     game_grid = AgentGameGrid(expecti_agent)

    # random = RandomAgent()
    # print(play_game(TwentyFortyEight()[0], random))

    # greedy = GreedyAgent()
    # game_grid = AgentGameGrid(greedy)

    # mcts = MCTSAgent(time_limit=0.1, objective='score')
    # game_grid = AgentGameGrid(mcts)

    q_learning_agent = ApproximateQAgent(time_limit = 100.0)
    print(play_game(TwentyFortyEight(), q_learning_agent))
