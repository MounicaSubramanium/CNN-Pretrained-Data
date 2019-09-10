# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.actions = {}

        # iterating over all states and over all possible actions from each of these states
        for _ in range(iterations):

            # complexity of each iteration is O(S*A*S); S is no. of states and A is all possible actions from that state
            new_stateValues = {}

            new_actionValue = {}

            # for each state iterate over the qvalue list
            for state in self.mdp.getStates():
                qvalue_list = []

                # get all possible actions which can be taken from this state
                possible_actions = mdp.getPossibleActions(state)

                # if len of all possible actions is 0 then
                if (len(possible_actions) == 0):

                    # assign new value to the new_state values
                    new_stateValues[state] = 0

                    # assign new value to the new action values
                    new_actionValue[state] = None

                # compute QValue for each action for this state and store it in actionValuePair dictionary
                else:
                    # for each action in possible iterate over the qvalue list
                    for action in possible_actions:

                        # append the state action pair to the list
                        qvalue_list.append((self.getQValue(state, action), action))

                    vvalue = max(qvalue_list)
                    new_stateValues[state] = vvalue[0]
                    new_actionValue[state] = vvalue[1]

            self.values = new_stateValues
            self.actions = new_actionValue

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        # assign q value to 0
        qvalue = 0

        # get the possible transition states and actions
        possible_tansition = self.mdp.getTransitionStatesAndProbs(state, action)

        # for each transition in list of possible transitions
        # transition[0] has the successor state (s-prime) represented in co-ordinates
        for transition in possible_tansition:

            # calculate reward transition
            reward = self.mdp.getReward(state, action, transition[0])

            # transition[1] has the probablity of reaching a particular successor state (s-prime) from state, action pair
            probability = transition[1]

            # get the utility value from tansition[0] which has successor state represented in coordinates
            utility_value = self.getValue(transition[0])

            # compute q value collectively using reward and probability transition
            qvalue = qvalue + (probability * (reward + (self.discount * utility_value)))

        # return q value
        return qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        if (len(self.actions) == 0):
            return None

        return self.actions[state]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)