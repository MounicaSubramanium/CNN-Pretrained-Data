# multiAgents.py
# --------------
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

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #get current position
        currentPosition = currentGameState.getPacmanPosition()

        #get the food list of the pacman
        currentFoodList = currentGameState.getFood().asList()

        #get the state of the ghost
        currentGhostStates = currentGameState.getGhostStates()


        curScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

        distance = float("inf")

        # for each ghost in new ghost state get its position currently
        for ghostState in newGhostStates:

            #get the position of ghost
            ghostPosition = ghostState.getPosition()

            # if the ghost is in new position
            if ghostPosition == newPos:

                # return - infinity
                return float("-inf")

        # for each food of pacman in current food list
        for food in currentFoodList:

            # get the distance between pacman and its food
            distance = min(distance, manhattanDistance(food, newPos))

            #if the direction stops then hald and return - infinity
            if Directions.STOP in action:

                return float("-inf")

        # returns the distance by incrementing one each time
        return 1.0 / (1.0 + distance)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def minimax_search(self, gameState, agentIndex, nodeDepth):

# if the index of agent is greater than the game state agents then
        if agentIndex >= gameState.getNumAgents():

            # return index of agent as 0
            agentIndex = 0

            # return node depth by incrementing 1 each time
            nodeDepth += 1


        # if depth of node is equal to the depth of agent itself
        if nodeDepth == self.depth:

            # return the distance finally for the game state
            return self.evaluationFunction(gameState)

        if agentIndex == self.index:

            return self.max_seacrh(gameState, agentIndex, nodeDepth)

        else:

            return self.min_search(gameState, agentIndex, nodeDepth)

        return 'None'

    def max_seacrh(self, gameState, agentIndex, nodeDepth):

        # if pacman has won or lose return the overall distance covered
        if gameState.isWin() or gameState.isLose():

            # return the distance from the function
            return self.evaluationFunction(gameState)

        #initialize value as - infinity
        value = float("-inf")

        #action value is none and initiated
        actionValue = "None"

        # get legal actions to be taken for the idex agent
        legalActions = gameState.getLegalActions(agentIndex)

        # for each action in list of legal actions
        for actions in legalActions:

            # if the action says stop continue
            if actions == Directions.STOP:

                continue;

            # get the successor of the node
            succ = gameState.generateSuccessor(agentIndex, actions)

            # get the minimax serach output in a temporary variable
            temp_var = self.minimax_search(succ, agentIndex + 1, nodeDepth)

            #if temporary variable is greater than the actual value
            if temp_var > value:

                # get the maximum value of temporary value and the actual value
                value = max(temp_var, value)

                # assign actions to the actual action value
                actionValue = actions

        if nodeDepth == 0:
            return actionValue

        else:
            return value

    def min_search(self, gameState, agentIndex, nodeDepth):

        # check if game state is win or lose
        if gameState.isWin() or gameState.isLose():

            # if win or lose retur nthe distance covered by pacman so far
            return self.evaluationFunction(gameState)

        # the initial distance va;lue will be - infinity
        value = float("inf")

        # give the action value to be none
        actionValue = "None"

        # get legal action to be taken for the index agent
        legalActions = gameState.getLegalActions(agentIndex)

        # ge tthe number of agents active in the game
        agentNumber = gameState.getNumAgents()

        # for each action in the list of legal actions

        for actions in legalActions:

            # if the action is stop then just stop there and continue with further steps of calculating the distance of agent covered so far
            if actions == Directions.STOP:
                continue;

            # get the successor of the current node
            succ = gameState.generateSuccessor(agentIndex, actions)

            # get the minimax search value for the successir node and store it in a temporary variable
            temp_var = self.minimax_search(succ, agentIndex + 1, nodeDepth)

            # if the minimax search value store in temporary variable is less than the actual value (-inf) then
            if temp_var < value:

                # get the minimum value of temporary variable and the actual value
                value = min(temp_var, value)

                # set actions to the action value variable
                actionValue = actions

        return value

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        return self.minimax_search(gameState, 0, 0)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def alpha_beta_search(self, gameState, agentIndex, nodeDepth, alpha, beta):

        # if the index of agent is greater than the number of the agents in the game
        if agentIndex >= gameState.getNumAgents():

            # initialize agent index to be zero
            agentIndex = 0

            # increment node depth by 1
            nodeDepth += 1

        if nodeDepth == self.depth:

            # return the depth or distance travelled by the agent in the game
            return self.evaluationFunction(gameState)

        #if index of agent represents the current agent itself return the max search value of alpha beta pruning
        if agentIndex == self.index:
            return self.max_seacrh(gameState, agentIndex, nodeDepth, alpha, beta)

        # else return the min search value of alpha beta pruning for that agent and node
        else:
            return self.min_search(gameState, agentIndex, nodeDepth, alpha, beta)

        # return none
        return 'None'

    def max_seacrh(self, gameState, agentIndex, nodeDepth, alpha, beta):

        # if the game state is win or lose
        if gameState.isWin() or gameState.isLose():

            # return the distance of the agent covered in pacman based on win or lose that is if the game has ended
            return self.evaluationFunction(gameState)

        # initial value will be - infinity
        value = float("-inf")

        #for each legal action in the list of legal actions of the agent obtained
        for legalActions in gameState.getLegalActions(agentIndex):

            # if the action says stop, just stop and return the distance so far covered
            if legalActions == Directions.STOP:
                continue

            # get the successor of the current node
            succ = gameState.generateSuccessor(agentIndex, legalActions)

            # get the alpha beta pruning value for the successor node and store it in a temporary variable
            temp_var = self.alpha_beta_search(succ, agentIndex + 1, nodeDepth, alpha, beta)

            # if temporary variable is greater than the value it self
            if temp_var > value:

                # get the temporary variable into the value var
                value = temp_var

                #get legal actions into action value variable
                actionValue = legalActions

            if value > beta:

                return value

                # max of alpha nd value is returned to the alpha varaible
            alpha = max(alpha, value)


        # if depth is zero return the action value itself
        if nodeDepth == 0:
            return actionValue

        # else return the actual value of the node
        else:
            return value


    def min_search(self, gameState, agentIndex, nodeDepth, alpha, beta):

        # if the game state is win or lose
        if gameState.isWin() or gameState.isLose():

            # return the distance of the agent covered in pacman based on win or lose that is if the game has ended
            return self.evaluationFunction(gameState)

        # initial value will be - infinity
        value = float("inf")


        # for each legal action in the list of legal actions of the agent obtained
        for legalActions in gameState.getLegalActions(agentIndex):

            # if the action says stop, just stop and return the distance so far covered
            if legalActions == Directions.STOP:
                continue

            # get the successor of the current node
            succ = gameState.generateSuccessor(agentIndex, legalActions)


            # get the alpha beta pruning value for the successor node and store it in a temporary variable
            temp_var = self.alpha_beta_search(succ, agentIndex + 1, nodeDepth, alpha, beta)

            # if temporary variable is less than the alpha value it self
            if temp_var < value:

                # get the temporary variable value into the value variable
                value = temp_var

                # get the legal actions into actual value variable
                actionValue = legalActions

            if value < alpha:
                return value

            # min of beta nd value is returned to the beta varaible
            beta = min(beta, value)

        return value

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        return self.alpha_beta_search(gameState, 0, 0, float("-inf"), float("inf"))


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectimax_value(self, gameState, agentIndex, nodeDepth):

        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            nodeDepth += 1

        if nodeDepth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == self.index:
            return self.max_seacrh(gameState, agentIndex, nodeDepth)
        else:
            return self.exp_value(gameState, agentIndex, nodeDepth)

        return 'None'

    def max_seacrh(self, gameState, agentIndex, nodeDepth):


        # if the game state is win or lose
        if gameState.isWin() or gameState.isLose():


            # return the distance of the agent covered in pacman based on win or lose that is if the game has ended
            return self.evaluationFunction(gameState)

        # initial value will be - infinity
        value = float("-inf")

        # the action value is stop at the moment
        actionValue = "Stop"


        # for each legal action in the list of legal actions of the agent obtained
        for legalActions in gameState.getLegalActions(agentIndex):


            # if the action says stop, just stop and return the distance so far covered
            if legalActions == Directions.STOP:
                continue

            # get the successor of the current node
            succ = gameState.generateSuccessor(agentIndex, legalActions)

            # get the alpha beta pruning value for the successor node and store it in a temporary variable
            temp_var = self.expectimax_value(succ, agentIndex + 1, nodeDepth)


            # if temporary variable is greater than the value it self
            if temp_var > value:

                # get the temporary variable value into the value variable
                value = temp_var

                # get the legal actions into action value variable
                actionValue = legalActions


        # if depth of current node is zero return the action value
        if nodeDepth == 0:
            return actionValue

        # else return the value itself
        else:
            return value

    def exp_value(self, gameState, agentIndex, nodeDepth):

        # if the game state is win or lose

        if gameState.isWin() or gameState.isLose():

            # return the distance of the agent covered in pacman based on win or lose that is if the game has ended
            return self.evaluationFunction(gameState)

        # initial value will be zero
        value = 0


        # calculate the probability value (1/distance covered by pacman)
        probabilityValue = 1.0 / len(gameState.getLegalActions(agentIndex))

        # for each legal action in the list of legal actions of the agent obtained
        for legalActions in gameState.getLegalActions(agentIndex):

            # if the action says stop, just stop and return the distance so far covered
            if legalActions == Directions.STOP:
                continue

            # get the successor of the current node
            succ = gameState.generateSuccessor(agentIndex, legalActions)

            # get the alpha beta pruning value for the successor node and store it in a temporary variable
            temp_var = self.expectimax_value(succ, agentIndex + 1, nodeDepth)


            # value is calculated by adding the product of probabiity value and temporary variable to the actual value
            value = value + (temp_var * probabilityValue)

            # get legal actions in the actual value varaible
            actionValue = legalActions

        return value

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax_value(gameState, 0, 0)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION:
      1. State with less number of food would be worth more
      2. A state where the pacmac meets a ghost is unfavourable
      3. The min distance between the pacman and a ghost
      4. Number of capsules in a state
      5.
    """
    "*** YOUR CODE HERE ***"

    # gee the current position of the pacman agent
    currentPosition = currentGameState.getPacmanPosition()

    #get the current food list of the agent to be covered
    currentFoodList = currentGameState.getFood().asList()

    # get teh current food count avaiable in the game
    currentFoodCount = currentGameState.getNumFood()

    # get the state of the ghost to calculate the path for the pacman agent
    currentGhostStates = currentGameState.getGhostStates()


    curScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]


    currentCapsules = currentGameState.getCapsules()

    # food left is calculated by the proportion of food count + 1
    foodLeft = 1.0 / (currentFoodCount + 1.0)


    # get current score of the agent
    currentScore = currentGameState.getScore()

    # distance of the ghost is initialized to +infinity initially
    ghostDistance = float("inf")


    scaredGhosts = 0

    # for each ghost state in the current ghost states
    for ghostState in currentGhostStates:

        # get teh position if the ghost
        ghostPosition = ghostState.getPosition()

        #if the current position is the position of the ghost then return -infinity
        if currentPosition == ghostPosition:

            return float("-inf")
        # else return the minimum of ghost distance and manhattan distance of the current pos of ghost
        else:

            ghostDistance = min(ghostDistance, manhattanDistance(currentPosition, ghostPosition))


        if ghostState.scaredTimer != 0:
            scaredGhosts += 1

    # initiallize the captured distance to be - infinity
    capsuledist = float("inf")


    #for each capsule the current capsule list
    for capsuleState in currentCapsules:

        # get the minimum of capsule distance and the manhattan distance of the current pos of the capsule
        capsuledist = min(capsuledist, manhattanDistance(currentPosition, capsuleState))


    # the ghost distance is calculated by the proportion of ghost distance with current ghost state
    ghostDistance = 1.0 / (1.0 + (ghostDistance / (len(currentGhostStates))))


    capsuledist = 1.0 / (1.0 + len(currentCapsules))

    scaredGhosts = 1.0 / (1.0 + scaredGhosts)


# return the current score of the agent along with food left for the pacman agent and ghost distance form the agent and the capsule distance
    return currentScore + (foodLeft + ghostDistance + capsuledist)


# Abbreviation
better = betterEvaluationFunction
