# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE

from copy import deepcopy

from games import Game

class TicTacToe(Game):
    def initial_state(self):
        """
        State is a dict with ONLY:
        - state["board"]: 3x3 list of lists, entries in {"X","O",None}
        - state["to_move"]: "X" or "O"
        """
        return {
            "to_move": "X",
            "board": [[None for _ in range(3)] for _ in range(3)]
        }

    def to_move(self, state):
        return state["to_move"]

    def actions(self, state):
        board = state["board"]
        actions = []
        for r in range(3):
            for c in range(3):
                if board[r][c] is None:
                    actions.append((r, c))
        return actions

    def result(self, state, action):
        r, c = action

        if not (0 <= r < 3 and 0 <= c < 3):
            raise ValueError("Move out of bounds")
        if state["board"][r][c] is not None:
            raise ValueError("Illegal move: cell occupied")

        player = state["to_move"]
        new_grid = deepcopy(state["board"])
        new_grid[r][c] = player

        return {
            "to_move": "O" if player == "X" else "X",
            "board": new_grid
        }

    def utility(self, state, player):
        winner = self._winner(state["board"])
        if winner is None:
            return 0
        return 1 if winner == player else -1

    def terminal_test(self, state):
        board = state["board"]
        return self._winner(board) is not None or all(
            board[r][c] is not None
            for r in range(3)
            for c in range(3)
        )

    def display(self, state):
        board = state["board"]
        for r in range(3):
            row = [
                board[r][c] if board[r][c] is not None else "."
                for c in range(3)
            ]
            print(" ".join(row))
        print("to_move:", state["to_move"])
        print()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _winner(self, board):
        lines = []

        # rows
        for r in range(3):
            lines.append([(r, c) for c in range(3)])

        # columns
        for c in range(3):
            lines.append([(r, c) for r in range(3)])

        # diagonals
        lines.append([(i, i) for i in range(3)])
        lines.append([(i, 2 - i) for i in range(3)])

        for line in lines:
            first = board[line[0][0]][line[0][1]]
            if first is None:
                continue
            if all(board[r][c] == first for r, c in line):
                return first

        return None

if __name__ == "__main__":
    game = TicTacToe()
    state = game.initial_state()
    game.display(state)

    while not game.terminal_test(state):
        # Getting input positions
        try:
            move = input("Enter your move as 'row col' (1-indexed): ")
            r, c = map(int, move.split())
        except ValueError:
            continue
        except KeyboardInterrupt:
            exit(0)
        if not (0 <= r - 1 <= 2 and 0 <= c - 1 <= 2):
            continue

        state = game.result(state, (r - 1, c - 1))
        game.display(state)

    winner = game._winner(state["board"])
    if winner is None:
        print("It's a draw!")
    else:
        print(f"{winner} wins!")
