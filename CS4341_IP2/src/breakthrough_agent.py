import time
import numpy as np


def minimax_cutoff_search(game, state, d=3, eval_fn=None):
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(current_state, depth):
        nonlocal expanded_nodes
        if game.terminal_test(current_state):
            return game.utility(current_state, player), None
        if depth == 0:
            return eval_fn(current_state, player), None

        expanded_nodes += 1
        v, best_act = -float('inf'), None
        legal_actions = game.actions(current_state)

        for a in legal_actions:
            v2, _ = min_value(game.result(current_state, a), depth - 1)
            if v2 > v:
                v, best_act = v2, a

        if best_act is None and legal_actions:
            best_act = legal_actions[0]

        return v, best_act

    def min_value(current_state, depth):
        nonlocal expanded_nodes
        if game.terminal_test(current_state):
            return game.utility(current_state, player), None
        if depth == 0:
            return eval_fn(current_state, player), None

        expanded_nodes += 1
        v, best_act = float('inf'), None
        legal_actions = game.actions(current_state)

        for a in legal_actions:
            v2, _ = max_value(game.result(current_state, a), depth - 1)
            if v2 < v:
                v, best_act = v2, a

        if best_act is None and legal_actions:
            best_act = legal_actions[0]

        return v, best_act

    _, move = max_value(state, d)
    return move, expanded_nodes

def alpha_beta_cutoff_search(game, state, d=4, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""
    player = game.to_move(state)
    expanded_nodes = 0

    def max_value(current_state, alpha, beta, depth):
        nonlocal expanded_nodes
        if game.terminal_test(current_state):
            return game.utility(current_state, player), None
        if depth == 0:
            return eval_fn(current_state, player), None

        expanded_nodes += 1
        v, best_act = -float('inf'), None
        legal_actions = game.actions(current_state)

        for a in legal_actions:
            v2, _ = min_value(game.result(current_state, a), alpha, beta, depth - 1)
            if v2 > v:
                v, best_act = v2, a
            if v >= beta:
                return v, best_act
            alpha = max(alpha, v)

        if best_act is None and legal_actions:
            best_act = legal_actions[0]

        return v, best_act

    def min_value(current_state, alpha, beta, depth):
        nonlocal expanded_nodes
        if game.terminal_test(current_state):
            return game.utility(current_state, player), None
        if depth == 0:
            return eval_fn(current_state, player), None

        expanded_nodes += 1
        v, best_act = float('inf'), None
        legal_actions = game.actions(current_state)

        for a in legal_actions:
            v2, _ = max_value(game.result(current_state, a), alpha, beta, depth - 1)
            if v2 < v:
                v, best_act = v2, a
            if v <= alpha:
                return v, best_act
            beta = min(beta, v)

        if best_act is None and legal_actions:
            best_act = legal_actions[0]

        return v, best_act

    _, move = max_value(state, -float('inf'), float('inf'), d)
    return move, expanded_nodes

##########################################################################


class BaseAgent:
    def __init__(self, name, depth, eval_fn):
        self.name = name
        self.depth = depth
        self.eval_fn = eval_fn
        self.time_per_move = []
        self.nodes_per_move = []

    def select_move(self, game, state):
        raise NotImplementedError

    def reset(self):
        self.time_per_move = []
        self.nodes_per_move = []


class RandomAgent(BaseAgent):
    def __init__(self, name="Random"):
        super().__init__(name, depth=0, eval_fn=None)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = np.random.choice(game.actions(state)), 1
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move


class MinimaxAgent(BaseAgent):
    def __init__(self, name, depth=3, eval_fn=None):
        super().__init__(name, depth, eval_fn)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = minimax_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move


class AlphaBetaAgent(BaseAgent):
    def __init__(self, name, depth=4, eval_fn=None):
        super().__init__(name, depth, eval_fn)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = alpha_beta_cutoff_search(game, state, self.depth, self.eval_fn)
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move
