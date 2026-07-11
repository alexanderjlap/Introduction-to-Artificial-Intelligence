import json

from breakthrough import offensive_eval_1, defensive_eval_1
from breakthrough import offensive_eval_2, defensive_eval_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent


# THIS FILE IS FOR PERFORMING EXPERIMENTS ON BREAKTHROUGH GAME
#   _____                            _              _
#  |_   _|                          | |            | |
#    | |  _ __ ___  _ __   ___  _ __| |_ __ _ _ __ | |_
#    | | | '_ ` _ \| '_ \ / _ \| '__| __/ _` | '_ \| __|
#   _| |_| | | | | | |_) | (_) | |  | || (_| | | | | |_
#  |_____|_| |_| |_| .__/ \___/|_|   \__\__,_|_| |_|\__|
#                  | |
#                  |_|
# YOUR NAME: Alexander Lap
# YOUR WPI ID: 633426257
# FINISH THE ASSIGNMENT IN `breakthrough.py` AND `breakthrough_agent.py`
#   After implementing breakthrough game, you may run GUI to check.
#   After implementing adversarial search and provided eval functions, you may
#       test against random agent.
#   Finally, perform the experiments required for the report here.
# REQUIRED PACKAGES: click, numpy, pygame, tqdm


##########################################################################
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
# Perform the necessary experiments here to generate data required by the report.

def main():
    matchups = [
        # 1) Minimax (Offensive Evaluation 1) vs Alpha-beta (Offensive Evaluation 1)
        (MinimaxAgent("Minimax Off1", depth=2, eval_fn=offensive_eval_1),
         AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)),

        # 2) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
        (AlphaBetaAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)),

        # 3) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
        (AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)),

        # 4) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Offensive Evaluation 1)
        (AlphaBetaAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Off1", depth=3, eval_fn=offensive_eval_1)),

        # 5) Alpha-beta (Defensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 1)
        (AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def1", depth=3, eval_fn=defensive_eval_1)),

        # 6) Alpha-beta (Offensive Evaluation 2) vs Alpha-beta (Defensive Evaluation 2)
        (AlphaBetaAgent("AlphaBeta Off2", depth=3, eval_fn=offensive_eval_2),
         AlphaBetaAgent("AlphaBeta Def2", depth=3, eval_fn=defensive_eval_2))
    ]

    print("=== Breakthrough Experiments ===")

    for i, (w_agent, b_agent) in enumerate(matchups, 1):
        print(f"\nRunning Matchup {i}: {w_agent.name} (White) vs {b_agent.name} (Black)")
        results = play_game(w_agent, b_agent, max_moves=400, display=False, display_final=False, progress=True)

        print(f"Winner: {results['winner']}")
        print(f"Total Moves: {results['total_moves']}")
        print(f"Nodes Expanded - White: {results['white_nodes']} | Black: {results['black_nodes']}")
        print(
            f"Avg Nodes/Move - White: {results['white_nodes_per_move']:.1f} | Black: {results['black_nodes_per_move']:.1f}")
        print(
            f"Avg Time/Move  - White: {results['white_time_per_move']:.4f}s | Black: {results['black_time_per_move']:.4f}s")
        print(f"Captures       - White: {results['white_captures']} | Black: {results['black_captures']}")

if __name__ == '__main__':
    main()
