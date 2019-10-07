import util
import heuristics as h
from hand import Hand
import parameters as p
import copy
import discrete_space as d


class FeatureExtractor:
    def __init__(self, target_key, heuristic_list):
        self.target_key = target_key  # the key we are aiming to hit.
        self.heuristic_list = heuristic_list

    def get_features(self, state: Hand, action):
        """
        used by the approximate qlearner to get the features of a certain state and action.
        :param state: the state, represented by the vector from the end of each bone to the target key.
        :param action: the action, a list of action for each bone of the hand.
        :return: features (util.Counter())
        """
        prob = FeatureProblem(self.target_key)
        features = util.Counter()
        hand = copy.deepcopy(state)  # we need to reconstruct the hand
        hand.move(action)
        if p.make_space_discrete == p.DISCRETE:
            next_state = d.get_hand_pos(hand)
            hand.move_to_discrete_position(next_state)

        for heuristic in self.heuristic_list:
            features[heuristic] = heuristic(hand, prob)

        return features


class FeatureProblem(h.Problem):
    def __init__(self, target_key):
        h.Problem.__init__(self)
        self.continuous_key = target_key  # the key we are aiming to hit.
        self.discrete_key = d.get_block(target_key)

    def get_goal(self):
        """ Returns discrete position if space is discrete and returns real position otherwise """
        if p.make_space_discrete == p.DISCRETE:
            return self.discrete_key
        return self.continuous_key
