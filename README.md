2048 with AI
===========

Based on the popular game [2048](https://github.com/gabrielecirulli/2048) by Gabriele Cirulli. The game's objective is to slide numbered tiles on a grid to combine them to create a tile with the number 2048. Created by [Duncan Du](https://github.com/Duncan-Du) and [Bhavya Kasera](https://github.com/bhavyakasera), this project explores different AI agents to play the popular mobile game, 2048. We implemented a Monte-Carlo Tree Search agent, an Expectimax agent, and a Linear Approximate Q-Learning agent. They are also compared with a random agent and a greedy agent. Feel free to play around yourself!

![screenshot](img/screenshot.png)

How to run the testing script - 
----------------------------------------------
The following packages are required to run the evaluation/visualization - 
```
tkinter
```

Evaluation : to evaluate an agent over a number of games, run the executable with the following arguments (num_games must be at least 2) -
python3 test.py [num_games] [random|greedy|expectimax|expectimax_smoothness|mcts|q_learning]
example usage:
```shell
python3 test.py 1000 mcts
```
Visualization : to visualize a game, run the executable with the following arguments -
```shell
python3 test.py vis [random|greedy|expectimax|expectimax_smoothness|mcts|q_learning]
```
Play : Try out the game yourself! Run the following, and use the arrows keys to move the tiles -
```shell
python3 test.py play
```

Credits:
==
2048 game python UI based on [this repo](https://github.com/yangshun/2048-python) by
- [Yanghun Tay](http://github.com/yangshun)
- [Emmanuel Goh](http://github.com/emman27)
