import random
from game import State
from agent import Agent
import math
import time

class MCTSAgent(Agent):

    def __init__(self, time_limit=0.1, objective = 'score'):
        super(MCTSAgent, self).__init__()
        self.time_limit = time_limit
        self.objective = objective


    def get_action(self, state: State):
        """
            Returns the action with the highest expected score
        """
        root = Node(state, objective=self.objective)
        start_time = time.time()
        count = 0
        while (time.time() - start_time) < self.time_limit:
            selected_node = select(root)
            if not selected_node.state.is_terminal():
                new_node = expand(selected_node)
                result = simulate(new_node)
                backpropagate(new_node, result)
            else:
                if self.objective=='score':
                    result = selected_node.state.get_score()
                else:
                    result = selected_node.state.has_2048()
                backpropagate(selected_node, result)
            count += 1
        # calculate average visits for the states generated by each action
        # pick the action with the highest average visits
        visits = [sum([child.visits for child in action])/len(action) for action in root.children]
        return root.children[visits.index(max(visits))][0].move
    
class Node:
    def __init__(self, state, move=None, parent=None, objective='score'):
        self.state = state
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.objective = objective

def ucb(node, exploration_weight=2.0):
    """
    use upper confidence bound to calculate exploitation, exploration values for nodes
    """
    if node.visits == 0:
        return float('inf')
    exploitation = node.value / node.visits
    exploration = exploration_weight * math.sqrt(math.log(node.parent.visits) / node.visits)
    return exploitation + exploration

def select(node):
    """
    select next node to traverse - first selects action with highest expected ucb value, 
    then picks a random successor state of that action
    """
    if not node.children:
        return node
    avg_ucbs = [sum([ucb(child) for child in action])/len(action) for action in node.children]
    i = avg_ucbs.index(max(avg_ucbs))
    return select(random.choice(node.children[i]))

def expand(node):
    """
    expand node
    """
    for action in node.state.get_actions():
        node.children.append([Node(succ_state, move=action, parent=node, objective=node.objective) for succ_state in node.state.get_successors(action)])
    return random.choice(random.choice(node.children))

def simulate(node):
    """
    simulate game to a terminal state
    """
    state = node.state
    while not state.is_terminal():
        action = random.choice(state.get_actions())
        state = random.choice(state.get_successors(action))
    if node.objective=='score':
        return state.get_score()
    else:
        return int(state.has_2048())

def backpropagate(node, result):
    """
    backpropagate payoff up the game tree
    """
    while node is not None:
        node.visits += 1
        node.value += result
        node = node.parent