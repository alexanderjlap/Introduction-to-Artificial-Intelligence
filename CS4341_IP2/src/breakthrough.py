import random
from copy import deepcopy

from tqdm import tqdm

from games import Game

# The template uses the defined Game class in games.py.
# Please read the source code for them, which includes comments.
# Also, you may refer to TicTacToe example for Breakthrough implementation.

class Breakthrough(Game):
    def initial_state(self): # ⚠️ DO NOT CHANGE THIS FUNCTION
        # Initial state should look like Figure 1 in the assignment specification.
        grid = [["EMPTY" for _ in range(8)] for _ in range(8)]
        for r in range(0, 2):
            for c in range(8):
                grid[r][c] = "BLACK"
        for r in range(6, 8):
            for c in range(8):
                grid[r][c] = "WHITE"
        return {
            'to_move': "WHITE",                   # Player is also a string "WHITE" or "BLACK".
            'captures': {"WHITE": 0, "BLACK": 0}, # Initially, white and black have captured 0 pieces.
            'board': grid,                        # 8x8 grid representing the board.
        } # ⚠️ You must use this structure for the state representation.

    def to_move(self, state):
        return state['to_move']

    def actions(self, state):
        player = state['to_move']
        board = state['board']
        actions = []

        direction = -1 if player == "WHITE" else 1
        opponent = "BLACK" if player == "WHITE" else "WHITE"

        for r in range(8):
            for c in range(8):
                if board[r][c] == player:
                    nr = r + direction
                    if 0 <= nr < 8:
                        # Move forward (must be empty)
                        if board[nr][c] == "EMPTY":
                            actions.append({"from": (r, c), "to": (nr, c)})
                        # Capture / Move diagonally left
                        if c - 1 >= 0 and board[nr][c - 1] in ["EMPTY", opponent]:
                            actions.append({"from": (r, c), "to": (nr, c - 1)})
                        # Capture / Move diagonally right
                        if c + 1 < 8 and board[nr][c + 1] in ["EMPTY", opponent]:
                            actions.append({"from": (r, c), "to": (nr, c + 1)})
        return actions

    def result(self, state, action):
        player = state['to_move']
        opponent = "BLACK" if player == "WHITE" else "WHITE"
        r1, c1 = action['from']
        r2, c2 = action['to']

        # Faster deepcopy for 2D list and dict
        new_board = [row[:] for row in state['board']]
        new_captures = state['captures'].copy()

        target_cell = new_board[r2][c2]
        if target_cell == opponent:
            new_captures[player] += 1

        new_board[r2][c2] = player
        new_board[r1][c1] = "EMPTY"

        return {
            'to_move': opponent,
            'captures': new_captures,
            'board': new_board
        }


    def utility(self, state, player):
        winner = self._get_winner(state)
        if winner is None:
            return 0
        return 1000000 if winner == player else -1000000


    def terminal_test(self, state):
        return self._get_winner(state) is not None


    def display(self, state):
        chars = {"WHITE": "W", "BLACK": "B", "EMPTY": "."}
        print("\n".join("".join(chars[state['board'][r][c]] for c in range(8)) for r in range(8)))
        if self.terminal_test(state):
            if self.to_move(state) == "WHITE":
                print("Black wins!")
            else:
                print("White wins!")
        else:
            print(f"To move: {state['to_move']}")
        print(f"Captures: White captured {state['captures']['WHITE']} pieces, Black captured {state['captures']['BLACK']} pieces")

    def _get_winner(self, state):
        if state['captures']['WHITE'] == 16:
            return "WHITE"
        if state['captures']['BLACK'] == 16:
            return "BLACK"
        for c in range(8):
            if state['board'][0][c] == "WHITE":
                return "WHITE"
            if state['board'][7][c] == "BLACK":
                return "BLACK"
        return None

def defensive_eval_1(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    own_remaining = 16 - state['captures'][opponent]
    return 2 * own_remaining + random.random()


def offensive_eval_1(state, player):
    opponent_remaining = 16 - state['captures'][player]
    return 2 * (32 - opponent_remaining) + random.random()


def defensive_eval_2(state, player):
    opponent = "BLACK" if player == "WHITE" else "WHITE"
    own_remaining = 16 - state['captures'][opponent]

    home_row_val = 0
    home_rows = [6, 7] if player == "WHITE" else [0, 1]
    for r in home_rows:
        for c in range(8):
            if state['board'][r][c] == player:
                home_row_val += 1

    return (2 * own_remaining) + (1.5 * home_row_val) + random.random()

def offensive_eval_2(state, player):
    opponent_remaining = 16 - state['captures'][player]

    advance_val = 0
    for r in range(8):
        for c in range(8):
            if state['board'][r][c] == player:
                advance_val += (7 - r) if player == "WHITE" else r

    return 2 * (32 - opponent_remaining) + (0.5 * advance_val) + random.random()

ag_eval_fn = defensive_eval_1           # ⚠️ Should be enough to pass AG test, but you may change it.
competition_eval_fn = defensive_eval_1  # ⚠️ Change this to your preferred evaluation function for comeptition.

##########################################################################

def play_game(white_agent, black_agent, max_moves=400, display=False, display_final=False, progress=False): # ⚠️ DO NOT CHANGE
    """
    Run a round of game with specified agents. Returns the statistic of the gameplay.

    :param white_agent: An agent that plays white.
    :param black_agent: An agent that plays black.
    :param max_moves: The maximum number of moves to play.
    :param display: Whether to display the game state during play.
    :param display_final: Whether to display the final game state.
    :param progress: Whether to show a progress bar.
    :return: The statistic of the game play.
    """
    game = Breakthrough()

    state = game.initial_state()
    move_count = 0
    if progress:
        pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100)
    while True:
        move = white_agent.select_move(game, state) if state["to_move"] == "WHITE" else black_agent.select_move(game, state)
        state = game.result(state, move)
        if display:
            game.display(state)
        move_count += 1
        if progress:
            pbar.update()
        if game.terminal_test(state) or move_count >= max_moves:
            if move_count <= max_moves:
                winner = "WHITE" if state["to_move"] == "BLACK" else "BLACK"
            else:
                winner = None
            break
    if progress:
        pbar.close()
    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)
    white_time_per_move = (sum(white_agent.time_per_move) / len(white_agent.time_per_move))
    black_time_per_move = (sum(black_agent.time_per_move) / len(black_agent.time_per_move))
    white_nodes_per_move = white_nodes / len(white_agent.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black_agent.nodes_per_move)
    white_captures = state["captures"]["WHITE"]
    black_captures = state["captures"]["BLACK"]
    if display or display_final:
        game.display(state)
    return {
        'final_state': state,
        'winner': 'white' if winner == "WHITE" else 'black' if winner == "BLACK" else None,
        'white_name': white_agent.name,
        'black_name': black_agent.name,
        'total_moves': move_count,
        'white_nodes': white_nodes,
        'black_nodes': black_nodes,
        'white_nodes_per_move': white_nodes_per_move,
        'black_nodes_per_move': black_nodes_per_move,
        'white_time_per_move': white_time_per_move,
        'black_time_per_move': black_time_per_move,
        'white_captures': white_captures,
        'black_captures': black_captures,
    }


if __name__ == '__main__':
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)
    black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)
    results = play_game(white_agent, black_agent, max_moves=400, display=False, display_final=True, progress=True)
    print(results)
