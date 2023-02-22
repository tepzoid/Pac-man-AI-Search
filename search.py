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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push(problem.getStartState())
    actions = util.Stack()
    expanded = []
    
    while not (frontier.isEmpty()):
        node = frontier.pop()
        if problem.isGoalState(node):
            print("Goalstate",node)
            path = actions.pop()
            return path

        if node not in expanded:
            expanded.append(node)
            children = []
            action = []
            if not(actions.isEmpty()):
                action = actions.pop()
            for triple in problem.getSuccessors(node):
                if(triple[0] not in expanded):    
                    newaction = []
                    for move in action:
                        newaction.append(move)
                    newaction.append(triple[1])
                    frontier.push(triple[0])
                    actions.push(newaction)

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    frontier.push([problem.getStartState(),0],0)
    expanded = []
    outerActions = util.PriorityQueue()
    while not (frontier.isEmpty()):
        nodeInfo = frontier.pop()
        node = nodeInfo[0]
        nodePriority = nodeInfo[1]
        innerActions = []
        if problem.isGoalState(node):
            print("Goalstate",node)
            path = outerActions.pop()
            return path

        

        if node not in expanded:
            parentAction = []
            expanded.append(node)
            if not(outerActions.isEmpty()):
                parentAction = outerActions.pop()
            for triple in problem.getSuccessors(node):
                if(triple[0] not in expanded): 
                    newAction = []   
                    for action in parentAction:
                        newAction.append(action)
                    newAction.append(triple[1])
                    frontier.push([triple[0],nodePriority+1],nodePriority+1)
                    innerActions.append(newAction)
        else:
            outerActions.pop()


        for i in range(len(innerActions)):
            outerActions.push(innerActions[i],nodePriority+1)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier  = util.PriorityQueue()
    frontier.push([problem.getStartState(),0],0)
    actions = util.PriorityQueue()
    expanded = []
    while(not(frontier.isEmpty())):
        node = frontier.pop()
        if (problem.isGoalState(node[0])):
            path = actions.pop()
            return path
        parentAction = []
        if not (actions.isEmpty()):
            parentAction = actions.pop()
        if node[0] not in expanded:
            expanded.append(node[0])
            for successor in problem.getSuccessors(node[0]):
                if(successor[0] not in expanded):
                    childAction = []
                    for move in parentAction:
                        childAction.append(move)
                    childAction.append(successor[1])
                    childCost = problem.getCostOfActions(childAction)
                    frontier.push([successor[0],childCost],childCost)
                    actions.push(childAction,childCost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier  = util.PriorityQueue()
    frontier.push([problem.getStartState(),0],0)
    actions = util.PriorityQueue()
    expanded = []
    while(not(frontier.isEmpty())):
        node = frontier.pop()
        if (problem.isGoalState(node[0])):
            path = actions.pop()
            return path
        parentAction = []
        if not (actions.isEmpty()):
            parentAction = actions.pop()
        if node[0] not in expanded:
            expanded.append(node[0])
            for successor in problem.getSuccessors(node[0]):
                if(successor[0] not in expanded):
                    childAction = []
                    for move in parentAction:
                        childAction.append(move)
                    childAction.append(successor[1])
                    hCost = heuristic(successor[0],problem)
                    childCost = problem.getCostOfActions(childAction)+hCost
                    frontier.push([successor[0],childCost],childCost)
                    actions.push(childAction,childCost)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
