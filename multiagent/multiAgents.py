# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        

        "*** YOUR CODE HERE ***"        
        
        foodList = newFood.asList()
        curCloseFoodDist = 999999
        for f in foodList:
            foodDist = manhattanDistance(f, newPos)
            curCloseFoodDist = min(foodDist, curCloseFoodDist)
        
        curFoodStates = currentGameState.getFood()
        newGhostPositions = [ghost.getPosition() for ghost in newGhostStates]
        for p in newGhostPositions:
            if p == newPos or manhattanDistance(p, newPos) == 1:
                return -999999
            elif curFoodStates[newPos[0]][newPos[1]]:
                return 999999
            else:
                return -curCloseFoodDist
              

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.
        """
        score = -999999

        """Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1"""

        #max agent-> pacman first
        curActions = gameState.getLegalActions(0)
        for a in curActions:
            succ = gameState.generateSuccessor(0, a)
            #next agent is Min: return min_value(state)
            curScore = self.min_value(succ, 0, 1)
            if curScore > score:
                score = curScore
                resultAction = a
        return resultAction
            


        "*** YOUR CODE HERE ***"
    #pacman
    def max_value(self, gameState, depth):
        v = -999999
        #현재 value값
        
         #terminated or maximum depth achieved
         #이긴 상황
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        #진 상황
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        #끝에 도달 했을때
        if depth+1 == self.depth:
            return self.evaluationFunction(gameState)
        
        actions = gameState.getLegalActions(0) 
        for a in actions:
            succ = gameState.generateSuccessor(0, a)
            v = max(v, self.min_value(succ, depth+1, 1))

        return v

    #ghosts
    def min_value(self, gameState, depth, agentIndex):
        v = 999999
         #terminated or maximum depth achieved
         #이긴 상황
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        #진 상황
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        #끝에 도달 했을때
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        
        curActions = gameState.getLegalActions(agentIndex)
        for a in curActions:
            succ = gameState.generateSuccessor(agentIndex, a)
            numOfGhosts = gameState.getNumAgents()
            if agentIndex < numOfGhosts -1:
                v = min(v, self.min_value(succ, depth, agentIndex+1))
            else:
                v = min(v, self.max_value(succ, depth))
                
        return v
    
    
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        score = -999999
        alpha = -999999
        beta = 999999

        """Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1"""

        #max agent-> pacman first
        curActions = gameState.getLegalActions(0)
        for a in curActions:
            succ = gameState.generateSuccessor(0, a)
            #다음 agent-> ghost
            curScore = self.min_version(succ, 0, 1, alpha, beta)
            if curScore > score:
                score = curScore
                resultAction = a
                alpha = max( (alpha, curScore) )
        return resultAction


    def max_version(self, gameState, depth, alpha, beta):
        v = -999999
       #terminated or maximum depth achieved
         #이긴 상황, 진상황
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #끝에 도달 했을때
        elif depth+1 == self.depth:
            return self.evaluationFunction(gameState)
        
        curActions = gameState.getLegalActions(0)

        for a in curActions:
            succ = gameState.generateSuccessor(0, a)
            v = max(v, self.min_version(succ, depth+1, 1, alpha, beta))
            if v > beta: return v
            alpha = max(alpha, v)
        return v

    def min_version(self, gameState, depth, agentIndex, alpha, beta):
        v = 999999
        #terminated or maximum depth achieved
         #이긴 상황, 진 상황
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        #끝에 도달 했을때
        elif depth == self.depth:
            return self.evaluationFunction(gameState)
        
        curActions = gameState.getLegalActions(agentIndex)
        #curBeta = beta
        for a in curActions:
            succ = gameState.generateSuccessor(agentIndex, a)
            numOfGhostsIndex = gameState.getNumAgents()-1
            #아직 움직일 ghost 더 남아 있는 경우
            if agentIndex < numOfGhostsIndex:
                v = min(v, self.min_version(succ, depth, agentIndex+1, alpha, beta) )
                if v < alpha: return v
                beta = min(beta, v)
            else:
                v = min(v, self.max_version(succ, depth, alpha, beta))
                if v < alpha: return v
                beta = min(beta, v)
        return v
    

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
