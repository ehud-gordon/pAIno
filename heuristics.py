import parameters
import discrete_space
from hand import Hand
import numpy as np


""" When working with the a_star_agent, use heuristics that get as parameters
    a state (hand object) and a problem. The problem object needs to have a
    method called get_goal() that returns the goal (next key to play) """


class Problem:
    """ Class that the heuristics use. Override these methods in other classes """
    def __init__(self):
        self.arr = np.array([0, 0, 0])

    def get_goal(self):
        return self.arr


def null_heuristic(state: Hand, problem: Problem):
    """ A trivial heuristic """
    return 0


def fingertip_distance(state: Hand, problem: Problem):
    """ Calculates the distance from the fingertip to the goal """
    tip = state.get_fingertip_pos()
    if parameters.make_space_discrete == parameters.DISCRETE:
        tip = discrete_space.get_block(tip)
    goal = problem.get_goal()
    dif = np.linalg.norm(np.array(goal) - np.array(tip))
    if parameters.make_space_discrete == parameters.DISCRETE:
        return dif/parameters.max_dist
    else:
        dist = dif - parameters.radius_from_key_goal
        if dist <= 0:
            return 0  # reached goal
        else:
            if dist < parameters.radius_crit_zone:
                return (dist + 2*parameters.radius_crit_zone)/parameters.max_dist
            return dist/parameters.max_dist


def angle_pointing(state: Hand, problem: Problem):
    """ This heuristic calculates the angle between the vector from the goal to the finger
        and from the goal to the pivot of the finger """
    if parameters.make_space_discrete == parameters.DISCRETE:
        goal = problem.get_goal()
        finger_tip = np.array(discrete_space.get_block(state.get_fingertip_pos()))
        finger_base = np.array(discrete_space.get_block(state.bones[-1].pivot))
        vec1 = finger_tip - goal
        vec2 = finger_base - goal
        angle = discrete_space.angle_between(vec1, vec2)
        return angle/(2*np.pi)
    else:
        # the continuous case is a bit more complicated. checks if the straight line between the
        # fingertip and the finger pivot intersects with a sphere of radius rad from the goal
        finger_tip = state.get_fingertip_pos()
        finger_base = state.bones[-1].pivot
        vec = finger_tip - finger_base
        vec = vec / np.linalg.norm(vec)
        goal = problem.get_goal() - finger_base
        # calculate the length of the perpendicular vector from goal to vec, using gram-schmidt
        prod = np.dot(vec, goal) * vec
        per = goal - prod
        dist = np.linalg.norm(per) - parameters.radius_from_key_goal
        if dist < 0:
            return 0
        else:
            return dist/parameters.max_dist


def heur_dist_from_boxes(hand: Hand, problem: Problem):
    num_of_joints_out_of_box = hand.how_many_joints_out_of_boxes()
    return num_of_joints_out_of_box/parameters.num_bones
