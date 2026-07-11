from problem import Node
from utils import memoize, PriorityQueue

def astar_search(problem, h=None):

    h = memoize(h or problem.h)

    frontier = PriorityQueue()
    explored = set()
    frontier_nodes = {}

    start_node = Node(problem.initial)
    f_start = start_node.path_cost + h(start_node.state)

    frontier.put(start_node.state, f_start)
    frontier_nodes[start_node.state] = start_node

    while frontier_nodes:
        state, priority = frontier.pop()
        node = frontier_nodes.pop(state)

        if problem.is_goal(state):
            return node

        explored.add(state)

        for action in problem.actions(state):
            child_state = problem.result(state, action)

            child_cost = node.path_cost + 1
            child_node = Node(child_state, node, action, child_cost)

            child_f = child_cost + h(child_state)

            if child_state not in explored and child_state not in frontier_nodes:
                frontier.put(child_state, child_f)
                frontier_nodes[child_state] = child_node

            elif child_state in frontier_nodes:
                if child_f < frontier[child_state]:
                    frontier.update_priority(child_state, child_f)
                    frontier_nodes[child_state] = child_node

    return None

def ucs_search(problem):
    """Uniform Cost Search (UCS) is a search algorithm that expands the least
    cost node in the search tree. It is a special case of A* search, so try to
    reuse the astar_search function."""

    return astar_search(problem, h=lambda state:0)
