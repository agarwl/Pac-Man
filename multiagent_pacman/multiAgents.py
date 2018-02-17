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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # print(newPos)
        # print(newFood)
        # print(newScaredTimes)

        if successorGameState.isWin():
          return float("inf")

        ghostPos =  currentGameState.getGhostPosition(1)
        ghostdist = min(util.manhattanDistance(newPos, ghostPos),2)
        foodlist = newFood.asList()
        closestFood = float("inf")
        foodspos = [min(closestFood, util.manhattanDistance(foodPos, newPos)) for foodPos in foodlist]
        foodPos = sorted(foodspos)
        closestFood = foodspos[0]

        "*** YOUR CODE HERE ***"
        x,y = newPos        
        return successorGameState.getScore()  - 5 * closestFood + 50 * ghostdist \
           + 100 * currentGameState.hasFood(x,y)


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

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        N = gameState.getNumAgents()

        def maxValue(gameState, depth, returnAction = False):
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          else:
            v = -float("inf")
            for action in gameState.getLegalActions(0):
                v_prev = v
                v = max(v, minValue(gameState.generateSuccessor(0,action), depth, 1))
                if returnAction:
                  if v > v_prev:
                    bestAction = action
            if returnAction:
              return bestAction
            else:
              return v

        def minValue(gameState, depth, ghostIndex):
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          else:
            v = float("inf")
            if ghostIndex != N - 1:
              for action in gameState.getLegalActions(ghostIndex):
                  v = min(v, minValue(gameState.generateSuccessor(ghostIndex, action), depth, ghostIndex+1))
            else:
              assert(ghostIndex == N - 1)
              for action in gameState.getLegalActions(ghostIndex):
                  v = min(v, maxValue(gameState.generateSuccessor(ghostIndex, action), depth - 1))
            return v

        return maxValue(gameState, self.depth, True)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        N = gameState.getNumAgents()
        def alpha_beta_search():
          alpha = -float("inf")
          beta = float("inf")
          return maxValue(gameState, self.depth, alpha, beta, True)

        def maxValue(gameState, depth, alpha, beta, returnAction = False):
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          else:
            v = -float("inf")
            for action in gameState.getLegalActions(0):
                v_prev = v
                v = max(v, minValue(gameState.generateSuccessor(0, action), depth, 1, alpha, beta))                  
                if returnAction:
                  if v > v_prev:
                    bestAction = action
                if v > beta:
                  break
                alpha = max(alpha, v)
            if returnAction:
              return bestAction
            else:
              return v

        def minValue(gameState, depth, ghostIndex, alpha, beta):
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          else:
            v = float("inf")
            if ghostIndex != N - 1:
              for action in gameState.getLegalActions(ghostIndex):
                  v = min(v, minValue(gameState.generateSuccessor(ghostIndex, action), \
                       depth, ghostIndex+1, alpha, beta))
                  if v < alpha:
                    break
                  beta = min(beta, v)
            else:
              assert(ghostIndex == N - 1)
              for action in gameState.getLegalActions(ghostIndex):
                  v = min(v, maxValue(gameState.generateSuccessor(ghostIndex, action), depth - 1, alpha, beta))
                  if v < alpha:
                    break
                  beta = min(beta, v)
            return v

        return alpha_beta_search()


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
        # util.raiseNotDefined()
        N = gameState.getNumAgents()

        def maxValue(gameState, depth, returnAction = False):
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          else:
            v = -float("inf")
            for action in gameState.getLegalActions(0):
                v_prev = v
                v = max(v, minValue(gameState.generateSuccessor(0,action), depth, 1))
                if returnAction:
                  if v > v_prev:
                    bestAction = action
            if returnAction:
              return bestAction
            else:
              return v

        def minValue(gameState, depth, ghostIndex):
          if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          else:
            v = 0
            actions = gameState.getLegalActions(ghostIndex)
            if ghostIndex != N - 1:
              for action in actions:
                  v += minValue(gameState.generateSuccessor(ghostIndex, action), depth, ghostIndex+1)
            else:
              for action in actions:
                  v += maxValue(gameState.generateSuccessor(ghostIndex, action), depth - 1)
            v /= len(actions)
            return v

        return maxValue(gameState, self.depth, True)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")
    score = scoreEvaluationFunction(currentGameState)
    newFood = currentGameState.getFood()
    foodPos = newFood.asList()
    closestfood = float("inf")
    for pos in foodPos:
        thisdist = util.manhattanDistance(pos, currentGameState.getPacmanPosition())
        if (thisdist < closestfood):
            closestfood = thisdist
    N = currentGameState.getNumAgents()
    ghostdist = float("inf")
    for i in xrange(1,N):
        nextdist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
        ghostdist = min(ghostdist, nextdist)
    
    score += 100 * min(ghostdist, 3)
    score -= 10 * closestfood
    score -= len(foodPos)
    return score



# Abbreviation
better = betterEvaluationFunction

