# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    """
    # Initializations
    # create a node in the beginning,
    # Node_vertex contains nodes which have been popped from the queue and the direction
    # from which they have been obtained

    node_vertex = {}

    node_vertex["par"] = None

    visited = list()

    # position - current node's position where start_state is obtained and added to stack

    node_vertex["position"] = problem.getStartState()

    node_vertex["dir"] = None

    # Initial node has no parent vertex and it is obvious
    frontier_stack = util.Stack()

    frontier_stack.push(node_vertex)

    # if the frontier_stack is not empty pop the current node vertex out of stack and
    # check if it is the goal state, keep exploring

    while not frontier_stack.isEmpty():

        # remove the prioritized node from the frontier_stack initially

        node_vertex = frontier_stack.pop()

        # get the current node
        cur_node = node_vertex["position"]

        # if current node is in explored list of nodes, then continue exploring rest of the nodes

        if cur_node in visited:
            continue

        # append the visited list with current node
        visited.append(cur_node)

        # check to see if the current node is the goal state
        if problem.isGoalState(cur_node):
            break

        # add child nodes to the frontier if they haven't been explored yet
        for node in problem.getSuccessors(cur_node):
            if node[0] not in visited:
                # print("node[0],node[1]:",node[0],node[1])
                # create a dictionary to store the current node and its parent, and direction as well
                child_nodes = {}

                # storing the successor and the parent of the successor(child node)
                child_nodes["position"] = node[0]

                child_nodes["dir"] = node[1]

                child_nodes["par"] = node_vertex

                # push child node into the frontier stack
                frontier_stack.push(child_nodes)

    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []

    # Find the path of the goal and dstore it
    while (not node_vertex["par"] == None):
        # Find the direction to proceed
        solution.insert(0, node_vertex["dir"])
        # find the parent
        node_vertex = node_vertex["par"]

    return solution
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    # Initializations
    # create a node in the beginning,
    # Node_vertex contains nodes which have been popped from the queue and the direction
    # from which they have been obtained

    node_vertex = {}
    node_vertex["par"] = None

    # position - current node's position where start_state is obtained and added to stack

    node_vertex["position"] = problem.getStartState()

    node_vertex["dir"] = None

    # Initial node has no parent vertex and it is obvious
    # Initializa a queue to use it as a frontier
    frontier_queue = util.Queue()

    # push the source vertex or start state into the queue
    frontier_queue.push(node_vertex)

    # Initialize explored list which basically keeps track of nodes that are visited
    visited = list()

    # if the frontier_queue is not empty pop the current node vertex out of queue and
    # check if it is the goal state, keep exploring
    while not frontier_queue.isEmpty():

        # remove the prioritized node from the frontier_queue initially
        node_vertex = frontier_queue.pop()

        cur_node = node_vertex["position"]

        # if current node is in explored list of nodes, then continue exploring rest of the nodes
        if cur_node in visited:
            continue

        visited.append(cur_node)

        # check to see if the current node is the goal state

        if problem.isGoalState(cur_node):
            break

        # add child nodes to the frontier_queue if they haven't been explored yet
        for node in problem.getSuccessors(cur_node):
            if node[0] not in visited:
                child_nodes = {}
                # storing the successor and the parent of the child node

                child_nodes["position"] = node[0]

                child_nodes["dir"] = node[1]

                child_nodes["par"] = node_vertex

                # push child node into the frontier stack
                frontier_queue.push(child_nodes)

    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []

    # Find the path of the goal and dstore it
    while (not node_vertex["par"] == None):

        # Find the direction to proceed

        solution.insert(0, node_vertex["dir"])
        # find the parent

        node_vertex = node_vertex["par"]
    return solution
    util.raiseNotDefined()


def uniformCostSearch(problem):

    # Initializations
    # create a node in the beginning,
    # Node_vertex contains nodes which have been popped from the queue and the direction
    # from which they have been obtained

    node_vertex = {}

    # Initial node has no parent vertex and it is obvious
    node_vertex["par"] = None

    # position - current node's position where start_state is obtained and added to stack

    node_vertex["position"] = problem.getStartState()

    node_vertex["dir"] = None

    # the path cost for start state is zero.
    node_vertex["cost"] = 0

    # Initialize a priority queue to use it as a frontier
    frontier_pqueue = util.PriorityQueue()

    # push the source vertex or start state into the queue
    frontier_pqueue.push(node_vertex, node_vertex["cost"])

    # Initialize explored list which basically keeps track of nodes that are visited
    visited = list()

    # if the frontier_queue is not empty pop the current node vertex out of queue and
    # check if it is the goal state, keep exploring

    while not frontier_pqueue.isEmpty():

        # remove the prioritized node from the frontier_pqueue initially
        node_vertex = frontier_pqueue.pop()

        cur_node = node_vertex["position"]
        cost = node_vertex["cost"]

        # if current node is in explored list of nodes, then continue exploring rest of the nodes
        if cur_node in visited:
            continue

        visited.append(cur_node)

        # check to see if the current node is the goal state

        if problem.isGoalState(cur_node):
            break

        # add child nodes to the frontier_queue if they haven't been explored yet

        for node in problem.getSuccessors(cur_node):

            if node[0] not in visited:
                child_nodes = {}
                # storing the successor and the parent of the child node
                child_nodes["position"] = node[0]

                child_nodes["dir"] = node[1]
                child_nodes["par"] = node_vertex
                child_nodes["cost"] = node[2] + cost

                # push child node into the frontier stack
                frontier_pqueue.push(child_nodes, child_nodes["cost"])

    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []

    # Find the path of the goal and store it

    while (not node_vertex["par"] == None):

        # Find the direction to proceed
        solution.insert(0, node_vertex["dir"])

        # find the parent
        node_vertex = node_vertex["par"]

    return solution
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    print("**********************************")
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    # Initializations
    # create a node in the beginning,
    # Node_vertex contains nodes which have been popped from the queue and the direction
    # from which they have been obtained

    node_vertex = {}

    # Initial node has no parent vertex and it is obvious
    node_vertex["par"] = None

    # position - current node's position where start_state is obtained and added to stack

    node_vertex["position"] = problem.getStartState()

    node_vertex["dir"] = None

    # the path cost for start state is zero.
    node_vertex["cost"] = 0

    node_vertex["heuristic"] = heuristic(node_vertex["position"], problem)

    # Initialize a priority queue to use it as a frontier
    frontier_pqueue = util.PriorityQueue()

    # push the source vertex or start state into the queue
    frontier_pqueue.push(node_vertex, node_vertex["cost"] + node_vertex["heuristic"])

    # Initialize explored list which basically keeps track of nodes that are visited
    visited = list()


    while not frontier_pqueue.isEmpty():

        # remove the prioritized node from the frontier_pqueue initially
        node_vertex = frontier_pqueue.pop()

        cur_node = node_vertex["position"]
        cost = node_vertex["cost"]

        # if current node is in explored list of nodes, then continue exploring rest of the nodes
        if cur_node in visited:
            continue
        visited.append(cur_node)

        # check to see if the current node is the goal state

        if problem.isGoalState(cur_node):
            break

        # add child nodes to the frontier_queue if they haven't been explored yet

        for node in problem.getSuccessors(cur_node):
            if node[0] not in visited:
                child_nodes = {}

                # storing the successor and the parent of the child node

                child_nodes["position"] = node[0]
                child_nodes["dir"] = node[1]
                child_nodes["par"] = node_vertex
                child_nodes["cost"] = node[2] + cost
                child_nodes["heuristic"] = heuristic(node[0], problem)

                # push child node into the frontier stack
                frontier_pqueue.push(child_nodes, child_nodes["heuristic"] + child_nodes["cost"])

    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []

    # Find the path of the goal and store it

    while (not node_vertex["par"] == None):

        # Find the direction to proceed
        solution.insert(0, node_vertex["dir"])

        # find the parent
        node_vertex = node_vertex["par"]

    return solution
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
