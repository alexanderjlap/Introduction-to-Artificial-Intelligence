# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE

"""Games or Adversarial Search (Chapter 5)"""

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def initial_state(self):
        """Return the initial state of the game."""
        raise NotImplementedError

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        raise NotImplementedError

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return NotImplementedError

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)
