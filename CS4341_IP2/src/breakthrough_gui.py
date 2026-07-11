# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE
# YOU SHOULD NOT HAVE TO MODIFY THIS FILE


import sys

import pygame
import pygame.gfxdraw

from breakthrough import Breakthrough


CELL = 64
MARGIN = 40
W = H = CELL * 8 + MARGIN * 2
BG_LIGHT = (245, 205, 160)
BG_DARK = (185, 125, 80)
BG_SEL = (118, 181, 197)


def draw_piece(surface, center, radius, base_color, ring_color):
    x, y = center
    pygame.gfxdraw.filled_circle(surface, x, y, radius, base_color)
    pygame.gfxdraw.aacircle(surface, x, y, radius, ring_color)
    pygame.gfxdraw.aacircle(surface, x, y, max(radius - 3, 1), ring_color)
    hx, hy = x - radius // 3, y - radius // 3
    pygame.gfxdraw.filled_circle(
        surface,
        hx,
        hy,
        max(radius // 3, 1),
        (
            min(base_color[0] + 25, 255),
            min(base_color[1] + 25, 255),
            min(base_color[2] + 25, 255),
        ),
    )


def draw_board(screen, game, state, selected=None, highlighted=None):
    screen.fill((240, 230, 220))
    for r in range(8):
        for c in range(8):
            col = BG_LIGHT if (r + c) % 2 == 0 else BG_DARK
            if (r, c) == selected:
                col = BG_SEL
            pygame.draw.rect(
                screen,
                col,
                (MARGIN + c * CELL, MARGIN + r * CELL, CELL, CELL),
                border_radius=6,
            )
    if highlighted:
        for tmp in highlighted:
            (r2, c2) = tmp["to"]
            pygame.draw.rect(
                screen,
                (150, 200, 255),
                (MARGIN + c2 * CELL, MARGIN + r2 * CELL, CELL, CELL),
                width=4,
                border_radius=6,
            )
    for r in range(8):
        for c in range(8):
            center = (MARGIN + c * CELL + CELL // 2, MARGIN + r * CELL + CELL // 2)
            radius = CELL // 2 - 8
            if state["board"][r][c] == "WHITE":
                draw_piece(screen, center, radius, (245, 245, 245), (200, 200, 200))
            elif state["board"][r][c] == "BLACK":
                draw_piece(screen, center, radius, (35, 35, 40), (80, 80, 90))


def main(white_agent, black_agent):
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Breakthrough")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    game = Breakthrough()
    state = game.initial_state()

    selected = None
    highlighted = []
    game_over = False

    running = True
    winner = None
    msg = ""
    while running:
        if winner is not None:
            msg = (
                "White wins! Press R to reset."
                if winner == "W"
                else "Black wins! Press R to reset."
            )
        else:
            msg = "White to move" if state["to_move"] == "WHITE" else "Black to move"
        draw_board(screen, game, state, selected, highlighted)
        screen.blit(font.render(msg, True, (20, 20, 20)), (MARGIN, 8))
        pygame.display.flip()

        human_turn = (state["to_move"] == "WHITE" and white_agent is None) or \
                     (state["to_move"] == "BLACK" and black_agent is None)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and game_over and e.key == pygame.K_r:
                # Reset game with R
                game = Breakthrough()
                state = game.initial_state()
                selected = None
                highlighted = []
                game_over = False
                if white_agent:
                    white_agent.reset()
                if black_agent:
                    black_agent.reset()
            elif e.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = e.pos
                c = (x - MARGIN) // CELL
                r = (y - MARGIN) // CELL
                if 0 <= r < 8 and 0 <= c < 8 and human_turn:
                    human_moved = False
                    if selected and (r, c) != selected:
                        mlist = [
                            m
                            for m in game.actions(state)
                            if m["from"] == selected and m["to"] == (r, c)
                        ]
                        if mlist:
                            state = game.result(state, mlist[0])
                            selected = None
                            highlighted = []
                            human_moved = True
                    if not human_moved:
                        if state["board"][r][c] == "WHITE" and state["to_move"] == "WHITE" or \
                           state["board"][r][c] == "BLACK" and state["to_move"] == "BLACK":
                            selected = (r, c)
                            highlighted = [
                                m
                                for m in game.actions(state)
                                if m["from"] == selected
                            ]
                        else:
                            selected = None
                            highlighted = []

        if not human_turn and not game_over and winner is None:
            if state["to_move"] == "WHITE" and white_agent:
                move = white_agent.select_move(game, state)
                state = game.result(state, move)
            elif state["to_move"] == "BLACK" and black_agent:
                move = black_agent.select_move(game, state)
                state = game.result(state, move)

        winner = None if not game.terminal_test(state) else ("W" if state["to_move"] == "BLACK" else "B")
        if winner is not None:
            game_over = True
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent
    from breakthrough import offensive_eval_1, defensive_eval_1
    from breakthrough import offensive_eval_2, defensive_eval_2

    white_agent = None                      # Setting agent to None will let human play.
    # white_agent = AlphaBetaAgent("AlphaBeta Off1", depth=4, eval_fn=offensive_eval_1)
    black_agent = None                      # Setting agent to None will let human play.
    # black_agent = AlphaBetaAgent("AlphaBeta Def1", depth=4, eval_fn=defensive_eval_1)

    main(white_agent, black_agent)
