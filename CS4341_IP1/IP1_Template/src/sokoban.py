from problem import Problem

class Sokoban(Problem):

    def __init__(self, board):

        self.walls = set()
        self.goals = set()

        boxes = set()
        player = None

        for r, row in enumerate(board):
            for c, char in enumerate(row):
                if char == '%':
                    self.walls.add((r, c))
                elif char == '.':
                    self.goals.add((r, c))
                elif char == 'P':
                    player = (r, c)
                elif char == 'b':
                    boxes.add((r, c))
                elif char == 'B':
                    boxes.add((r, c))
                    self.goals.add((r, c))

        initial_state = (player, frozenset(boxes))

        super().__init__(initial_state)

    def actions(self, state):

        valid_actions = []
        player, boxes = state
        r, c = player

        direction = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1),
        }

        for action, (dr, dc) in direction.items():
            new_r, new_c = r + dr, c + dc
            new_pos = (new_r, new_c)

            if new_pos in self.walls:
                continue

            if new_pos in boxes:
                push_r, push_c = new_r + dr, new_c + dc
                push_pos = (push_r, push_c)

                if push_pos in self.walls or push_pos in boxes:
                    continue

            valid_actions.append(action)

        return valid_actions

    def result(self, state, action):

        player, boxes = state
        r, c = player

        direction = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1),
        }
        dr, dc = direction[action]

        new_pos = (r + dr, c + dc)
        new_boxes = set(boxes)

        if new_pos in new_boxes:
            new_boxes.remove(new_pos)
            push_pos = (new_pos[0] + dr, new_pos[1] + dc)
            new_boxes.add(push_pos)

        return (new_pos, frozenset(new_boxes))

    def is_goal(self, state):
        _, boxes = state
        return boxes == self.goals

    def h(self, state):
        _, boxes = state
        total_distance = 0

        for box in boxes:
            min_dist = float('inf')
            for goal in self.goals:
                dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                if dist < min_dist:
                    min_dist = dist
            total_distance += min_dist

        return total_distance
