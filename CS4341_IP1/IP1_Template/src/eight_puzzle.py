# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE

from problem import Problem


class EightPuzzle(Problem):
    """
    State is a tuple of length 9.
    0 represents the blank.
    Example:
        (1, 2, 3,
         4, 5, 6,
         7, 8, 0)
    """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(initial, goal)

    @staticmethod
    def find_blank_square(state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        blank = self.find_blank_square(state)

        if blank % 3 == 0:
            possible_actions.remove("LEFT")
        if blank < 3:
            possible_actions.remove("UP")
        if blank % 3 == 2:
            possible_actions.remove("RIGHT")
        if blank > 5:
            possible_actions.remove("DOWN")

        return possible_actions

    def result(self, state, action):
        if action not in self.actions(state):
            raise ValueError("Illegal move")

        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {
            "UP": -3,
            "DOWN": 3,
            "LEFT": -1,
            "RIGHT": 1
        }

        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    @staticmethod
    def check_solvability(state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inversion += 1
        return inversion % 2 == 0

    def display(self, state):
        for r in range(3):
            row = []
            for c in range(3):
                value = state[r * 3 + c]
                row.append(str(value) if value != 0 else ".")
            print(" ".join(row))
        print()

    def parse_action(self, text):
        """
        Accept:
            UP, DOWN, LEFT, RIGHT
            up, down, left, right
            w, a, s, d
            W, A, S, D
        Return canonical action string or None if invalid.
        """
        move = text.strip().upper()

        aliases = {
            "UP": "UP",
            "DOWN": "DOWN",
            "LEFT": "LEFT",
            "RIGHT": "RIGHT",
            "W": "UP",
            "S": "DOWN",
            "A": "LEFT",
            "D": "RIGHT",
        }

        return aliases.get(move)


if __name__ == "__main__":
    # You can change this starting state if you want.
    initial_state = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    puzzle = EightPuzzle(initial_state, goal_state)
    state = puzzle.initial

    if not puzzle.check_solvability(state):
        print("This puzzle is not solvable.")
        exit(0)

    print("Eight Puzzle")
    print("Enter moves: UP DOWN LEFT RIGHT")
    print("You can also type: w a s d")
    print("Blank tile is shown as .")
    print()

    puzzle.display(state)

    while not puzzle.goal_test(state):
        try:
            move_text = input("Enter the move of the blank tile: ")
        except KeyboardInterrupt:
            exit(0)

        action = puzzle.parse_action(move_text)
        if action is None:
            continue

        if action not in puzzle.actions(state):
            continue

        state = puzzle.result(state, action)
        puzzle.display(state)

    print("Goal reached!")