import random, util


class QLearningAgent:
    """ Q-Learning Agent """
    def __init__(self, epsilon=0.5, alpha=0.5, gamma=1):
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.ignore_zero = False
        self.Q = util.Counter()  # Q will have keys as tuple(state,action).

    def get_legal_actions(self, hand):
        """ Get the actions available for a given
            state. This is what you should use to
            obtain legal actions for a state """
        return hand.get_legal_actions()

    def get_q_value(self, state, action):
        """ Returns Q(state,action) """
        return self.Q[(state, action)]

    def get_value(self, state, hand):
        """ Returns max_action Q(state,action)
            where the max is over legal actions """
        legal_actions = list(self.get_legal_actions(hand))
        if not legal_actions:
            return 0
        random.shuffle(legal_actions)
        max_q = max(legal_actions, key=lambda action: self.get_q_value(state, action))
        return self.get_q_value(state, max_q)

    def get_policy(self, state, hand):
        """ Compute the best action to take in a state """
        legal_actions = list(self.get_legal_actions(hand))
        if not legal_actions:
            return None
        random.shuffle(legal_actions)
        max_action = legal_actions[0]
        # ignore unknown actions after learning
        if self.ignore_zero:
            for act in legal_actions:
                if self.get_q_value(state, act) != 0:
                    max_action = act
                    break
        max_q = self.get_q_value(state, max_action)
        for action in legal_actions:
            # if q value is bigger than max and either ignore zero=false or q value is not 0
            if self.get_q_value(state, action) > max_q and (not self.ignore_zero or self.get_q_value(state, action) != 0):
                max_q = self.get_q_value(state, action)
                max_action = action
        return max_action

    def get_action(self, state, hand):
        """ Compute the action to take in the current state """
        # Pick Action
        legal_actions = self.get_legal_actions(hand)
        random_action = random.choice(legal_actions)
        best_policy = self.get_policy(state, hand)
        return random_action if util.flipCoin(self.epsilon) else best_policy

    def update(self, state, action, next_state, reward, hand):
        """ Updates the Q values according to action and reward """
        self.Q[(state, action)] += self.alpha * (
            reward + self.discount * self.get_value(next_state, hand) - self.Q[(state, action)])


class ApproximateQAgent(QLearningAgent):
    """ ApproximateQLearningAgent """

    def __init__(self, epsilon, gamma, alpha, feature_extractor=None):
        QLearningAgent.__init__(self, epsilon=epsilon, alpha=alpha, gamma=gamma)
        self.feature_extractor = feature_extractor
        self.w = util.Counter()  # the weights for the features.

    def get_q_value(self, state, action):
        """ Should return Q(state,action) = w * featureVector
            where * is the dotProduct operator """
        features =  self.feature_extractor.get_features(state, action)
        # for i in self.w:
        #     print (self.w[i])
        return self.w * features

    def update(self, state, action, next_state, reward, hand):
        """ Should update your weights based on transition """
        features = self.feature_extractor.get_features(state, action)
        correction = reward + self.discount * self.get_value(next_state, hand) - self.get_q_value(state, action)

        for feature in features:
            # print(self.alpha)
            self.w[feature] += self.alpha * correction * features[feature]
            # print(self.w[feature])

