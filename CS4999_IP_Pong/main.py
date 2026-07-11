import math
import random
import sys
from collections import defaultdict

import pygame

# --- HYPERPARAMETERS & CONSTANTS ---
PADDLE_HEIGHT = 0.2
GRID_SIZE = 12
C_LEARNING_RATE = 100
GAMMA = 0.95
EPSILON = 0.05
TRAINING_GAMES = 100000

# --- GUI CONSTANTS ---
WINDOW_SIZE = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)


class PongEnvironment:
    """
    Simulates the Single-Player Pong environment and tracks the continuous
    state variables, handling physics and collision detection.
    """

    def __init__(self):
        self.ball_x = 0.0
        self.ball_y = 0.0
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.paddle_y = 0.0
        self.reset()

    def reset(self):
        """
        Resets the environment to the initial starting state.

        Returns:
            The discretized initial state as a tuple.
        """
        self.ball_x = 0.5
        self.ball_y = 0.5
        self.velocity_x = 0.03
        self.velocity_y = 0.01
        self.paddle_y = 0.5 - PADDLE_HEIGHT / 2
        return self.get_discrete_state()

    def step(self, action):
        """
        Advances the simulation by one time step based on the agent's action.

        Args:
            action (int): 0 = stay, 1 = move up, 2 = move down.

        Returns:
            A tuple containing (next_discrete_state, reward, is_terminal_boolean).
        """
        # Apply paddle movement
        if action == 1:
            self.paddle_y -= 0.04
        elif action == 2:
            self.paddle_y += 0.04

        # Enforce screen boundaries for the paddle
        if self.paddle_y < 0:
            self.paddle_y = 0
        elif self.paddle_y > 1 - PADDLE_HEIGHT:
            self.paddle_y = 1 - PADDLE_HEIGHT

        # Apply velocity to ball position
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        reward = 0
        terminal = False

        # Handle Top / Bottom Wall Collisions
        if self.ball_y < 0:
            self.ball_y = -self.ball_y
            self.velocity_y = -self.velocity_y
        elif self.ball_y > 1:
            self.ball_y = 2 - self.ball_y
            self.velocity_y = -self.velocity_y

        # Handle Left Wall Collision
        if self.ball_x < 0:
            self.ball_x = -self.ball_x
            self.velocity_x = -self.velocity_x

        # Handle Right Side (Paddle Collision or Miss)
        if self.ball_x >= 1:
            if self.paddle_y <= self.ball_y <= self.paddle_y + PADDLE_HEIGHT:
                # Successful paddle hit
                self.ball_x = 2 - self.ball_x

                # Apply random variation to velocities upon hit
                u = random.uniform(-0.015, 0.015)
                v = random.uniform(-0.03, 0.03)

                self.velocity_x = -self.velocity_x + u
                self.velocity_y = self.velocity_y + v

                # Enforce minimum x-velocity threshold
                if abs(self.velocity_x) < 0.03:
                    self.velocity_x = 0.03 if self.velocity_x > 0 else -0.03

                reward = 1
            else:
                # Ball bypassed paddle
                reward = -1
                terminal = True

        return self.get_discrete_state(), reward, terminal

    def get_discrete_state(self):
        """
        Converts the continuous state variables into a discretized state space
        representation for the Q-learning algorithm.

        Returns:
            The state representation. This is "TERMINAL" if the state is terminal,
            otherwise it returns a tuple of (grid_x, grid_y, v_x, v_y, paddle_pos).
        """
        if self.ball_x >= 1:
            return "TERMINAL"

        # Map continuous (0.0 - 1.0) positions to an integer grid
        discrete_x = min(int(math.floor(GRID_SIZE * self.ball_x)), GRID_SIZE - 1)
        discrete_y = min(int(math.floor(GRID_SIZE * self.ball_y)), GRID_SIZE - 1)

        # Catch float edge cases
        discrete_x = max(0, discrete_x)
        discrete_y = max(0, discrete_y)

        # Discretize X Velocity (Left or Right)
        v_x = 1 if self.velocity_x > 0 else -1

        # Discretize Y Velocity (5 bins for finer resolution)
        if self.velocity_y < -0.02:
            v_y = -2  # Fast Up
        elif self.velocity_y < -0.005:
            v_y = -1  # Slow Up
        elif self.velocity_y <= 0.005:
            v_y = 0  # Flat
        elif self.velocity_y <= 0.02:
            v_y = 1  # Slow Down
        else:
            v_y = 2  # Fast Down

        # Discretize Paddle Position
        discrete_paddle = int(math.floor(GRID_SIZE * self.paddle_y / (1 - PADDLE_HEIGHT)))
        if self.paddle_y >= 1 - PADDLE_HEIGHT:
            discrete_paddle = GRID_SIZE - 1

        return discrete_x, discrete_y, v_x, v_y, discrete_paddle


def train_agent():
    """
    Trains the Q-learning agent by simulating the environment over a set
    number of episodes using an epsilon-greedy exploration strategy.

    Returns:
        The converged Q-table mapping states to action values.
    """
    env = PongEnvironment()

    # Q-table: maps state -> list of 3 Q-values (one for each action)
    Q = defaultdict(lambda: [0.0, 0.0, 0.0])
    # N-table: counts visits to (state, action) for learning rate decay
    N = defaultdict(lambda: [0, 0, 0])

    for episode in range(TRAINING_GAMES):
        state = env.reset()
        terminal = False

        while not terminal:
            # Determine action via Epsilon-greedy policy
            if random.random() < EPSILON:
                action = random.choice([0, 1, 2])
            else:
                max_q = max(Q[state])
                best_actions = [a for a, q in enumerate(Q[state]) if q == max_q]
                action = random.choice(best_actions)

            next_state, reward, terminal = env.step(action)

            # Apply learning rate decay formula: C / (C + N(s,a))
            N[state][action] += 1
            alpha = C_LEARNING_RATE / (C_LEARNING_RATE + N[state][action])

            # Apply Bellman equation to update Q-value
            if terminal:
                max_q_next = 0.0
            else:
                max_q_next = max(Q[next_state])

            Q[state][action] += alpha * (reward + GAMMA * max_q_next - Q[state][action])
            state = next_state

        # Progress tracking
        if (episode + 1) % 10000 == 0:
            print(f"Completed {episode + 1} training games...")

    return Q


def test_agent(Q, test_games=1000):
    """
    Evaluates the trained agent's performance by running games using a
    strictly greedy policy (no exploration).

    Args:
        Q: The trained Q-table.
        test_games (int): The number of games to simulate.
    """
    env = PongEnvironment()
    total_bounces = 0

    for _ in range(test_games):
        state = env.reset()
        terminal = False
        bounces = 0

        while not terminal:
            # Strictly greedy action selection
            max_q = max(Q[state])
            best_actions = [a for a, q in enumerate(Q[state]) if q == max_q]
            action = random.choice(best_actions)

            state, reward, terminal = env.step(action)
            if reward == 1:
                bounces += 1

        total_bounces += bounces

    avg_bounces = total_bounces / test_games
    print(f"\n--- Testing Complete ---")
    print(f"Average bounces per game over {test_games} games: {avg_bounces:.2f}")


def play_gui(Q):
    """
    Runs a real-time graphical simulation of the trained agent using PyGame.

    Args:
        Q: The trained Q-table used to guide the paddle.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("CS 4999 Pong Agent - Trained via Q-Learning")
    clock = pygame.time.Clock()

    env = PongEnvironment()
    state = env.reset()

    font = pygame.font.SysFont(None, 36)
    bounces = 0
    max_bounces = 0

    running = True
    terminal = False

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if terminal:
            # Pause briefly upon missing the ball before resetting
            pygame.time.delay(1000)
            state = env.reset()
            bounces = 0
            terminal = False

        # --- Agent Decision Making ---
        max_q = max(Q[state])
        best_actions = [a for a, q in enumerate(Q[state]) if q == max_q]
        action = random.choice(best_actions)

        # Step the physics environment
        state, reward, terminal = env.step(action)

        if reward == 1:
            bounces += 1
            if bounces > max_bounces:
                max_bounces = bounces

        # --- Rendering ---
        screen.fill(WHITE)

        # Draw Ball
        ball_radius = int(WINDOW_SIZE * 0.02)
        ball_pos = (int(env.ball_x * WINDOW_SIZE), int(env.ball_y * WINDOW_SIZE))
        pygame.draw.circle(screen, RED, ball_pos, ball_radius)

        # Draw Paddle
        paddle_width = int(WINDOW_SIZE * 0.02)
        paddle_height_px = int(WINDOW_SIZE * PADDLE_HEIGHT)
        paddle_x_px = WINDOW_SIZE - paddle_width
        paddle_y_px = int(env.paddle_y * WINDOW_SIZE)
        pygame.draw.rect(screen, BLACK, (paddle_x_px, paddle_y_px, paddle_width, paddle_height_px))

        # Draw Left Wall
        pygame.draw.rect(screen, BLUE, (0, 0, 5, WINDOW_SIZE))

        # Draw Score
        score_text = font.render(f"Current Bounces: {bounces} | Max Bounces: {max_bounces}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Limit framerate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print("Training agent for 100,000 games... (Please wait a few seconds)")
    trained_Q = train_agent()

    print("\nRunning 1,000 headless test games to get average...")
    test_agent(trained_Q, test_games=1000)

    print("\nLaunching PyGame GUI! Watch your agent play.")
    play_gui(trained_Q)