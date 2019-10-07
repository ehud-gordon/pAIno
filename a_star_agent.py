import numpy as np
import util, copy
from hand import Hand
import parameters as p
import heuristics as h
import discrete_space


class SearchProblem(h.Problem):
    def __init__(self, hand, end_pos):
        h.Problem.__init__(self)
        self.expanded = 0
        self.hand = copy.deepcopy(hand)
        self.end_pos = end_pos
        if p.make_space_discrete == p.DISCRETE:
            self.end_pos_block = discrete_space.get_block(self.end_pos)

    def get_start_state(self):
        """ Returns the start state for the search problem """
        return self.hand

    def get_goal(self):
        if p.make_space_discrete == p.DISCRETE:
            return self.end_pos_block
        return self.end_pos

    def is_goal_state(self, state):
        """ state: Search state
            Returns True if and only if the state is a valid goal state """
        if p.make_space_discrete == p.DISCRETE:
            return discrete_space.get_block(state.get_fingertip_pos()) == self.end_pos_block
        else:
            return np.linalg.norm(state.get_fingertip_pos()-self.end_pos) < p.radius_from_key_goal

    def get_successors(self, state: Hand):
        """ state: Search state
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor """
        self.expanded += 1
        if self.expanded % 300 == 0:
            print("self.expanded = ", self.expanded)
        actions = state.get_legal_actions()
        successor_list = []
        for act in actions:
            dummy = copy.deepcopy(state)
            dummy.move(act)
            if p.make_space_discrete == p.DISCRETE:
                dummy.move_to_discrete_position(discrete_space.get_hand_pos(dummy))
            successor_list.append((dummy, act, 1))  # successor, move, stepCost
        return successor_list


def a_star_search(problem, heuristic=h.null_heuristic):
    """ Search the node that has the lowest combined cost and heuristic first """
    counter, offset = 0, 4
    visited = set()
    fringe = util.PriorityQueue()
    state = problem.get_start_state()  # hand
    # heur, step cost, costSoFar, counter, state, parent, move, cost
    node = [heuristic(state, problem), 0, 0, counter, state, None, None, 0]
    fringe.push(node, 0 + node[0])
    while not fringe.isEmpty():
        node = fringe.pop()
        if node[offset] not in visited:
            if problem.is_goal_state(node[offset]):
                break
            visited.add(node[offset])
            for child in problem.get_successors(node[offset]):  # successor, move, stepCost
                if child[0] not in visited:
                    counter += 1
                    heur = heuristic(child[0], problem)
                    fringe.push([heur, child[2], node[offset+3], counter, child[0],
                                 node, child[1], (node[offset+3] + child[2])],
                                (node[offset+3] + child[2] + heur))

    if not problem.is_goal_state(node[offset]):
        raise_incomplete()
    path = []
    while node[offset+2] is not None:
        path.insert(0, node[offset+2])
        node = node[offset+1]
    return path


def raise_incomplete():
    import sys
    print("A*, The given problem has no solution")
    sys.exit(0)
