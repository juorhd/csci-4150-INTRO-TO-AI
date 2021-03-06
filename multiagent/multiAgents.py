# multiAgents.py
# --------------
# Licensing INFormation:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution INFormation: The Pacman AI projects were developed at UC Berkeley.
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

        The code below extracts some useful INFormation from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful INFormation you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        curPos = currentGameState.getPacmanPosition()
        curFoodList = currentGameState.getFood().asList()
        curGhostStates = currentGameState.getGhostStates()
        curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]

        distance = float("INF")
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            if ghostPos == newPos:
                return float("-INF")
        
            for food in curFoodList:
                distance = min(distance,manhattanDistance(food,newPos))
            if Directions.STOP in action:  
                return float("-INF")

        return 1.0 / (1.0+distance)
        

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
        val = float("-INF")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = minimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            
            if temp > val:
                val = temp
                bestAction = successor[0]
        return bestAction
        
def minimax(agent, agentList, state, depth, evalFunc):
  
    if depth <= 0 or state.isWin() or state.isLose():
        return evalFunc(state)
    
    if agent == 0:
        val = float("-INF")
    else:
        val = float("INF")
          
    actions = state.getLegalActions(agent)
    successors = [state.generateSuccessor(agent, action) for action in actions]
    for j in range(len(successors)):
        successor = successors[j];
    
        if agent == 0:
            val = max(val, minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
            
        elif agent == agentList[-1]:
            val = min(val, minimax(agentList[0], agentList, successor, depth - 1, evalFunc))
            
        else:
            val = min(val, minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
  
    return val

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def AlphaBetaPrune(state):
          value, bestAction = None, None
          a, b = None, None

          for action in state.getLegalActions(0):
            value = max(value, minValue(state.generateSuccessor(0, action), 1, 1, a, b) )

            if a is None:
              a = value
              bestAction = action
            else:
              a, bestAction = max(value, a), action if value > a else bestAction
          return bestAction

        def minValue(state, agentIdx, ply, a, b):

          if agentIdx == state.getNumAgents():
            return maxValue(state, 0, ply + 1, a, b)

          value = None

          for action in state.getLegalActions(agentIdx):
            succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, ply, a, b)
            value = succ if value is None else min(value, succ)
            if a is not None and value < a:
              return value

            b = value if b is None else min(b, value)

          if value is not None:
            return value
          else:
            return self.evaluationFunction(state)


        def maxValue(state, agentIdx, ply, a, b):
          if ply > self.depth:
            return self.evaluationFunction(state)

          value = None

          for action in state.getLegalActions(agentIdx):
            succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, ply, a, b)
            value = max(value, succ)
            if b is not None and value > b:
              return value
            a = max(a, value)

          if value is not None:
            return value
          else:
            return self.evaluationFunction(state)

        action = AlphaBetaPrune(gameState)

        return action  
        
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
        v = float("-INF")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = expectimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            
            if temp > v:
              v = temp
              bestAction = successor[0]
        return bestAction
        

def expectimax(agent, agentList, state, depth, evalFunc):
  
  if depth <= 0 or state.isWin() or state.isLose():
    return evalFunc(state)
    
  if agent == 0:
    v = float("-INF")
  else:
    v = 0
          
  actions = state.getLegalActions(agent)
  successors = [state.generateSuccessor(agent, action) for action in actions]
  p = 1.0/len(successors)
  for j in range(len(successors)):
    successor = successors[j];
    
    if agent == 0:
      
      v = max(v, expectimax(agentList[agent+1], agentList, successor, depth, evalFunc))
    elif agent == agentList[-1]:
      
      v += p * expectimax(agentList[0], agentList, successor, depth - 1, evalFunc)
    else:
     
      v += p * expectimax(agentList[agent+1], agentList, successor, depth, evalFunc)
  
  return v


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: 
      1. State with less number of food would be worth more
      2. A state where the pacmac meets a ghost is unfavourable
      3. The min distance between the pacman and a ghost
      4. Number of capsules in a state
    """
    "*** YOUR CODE HERE ***"
    curPos = currentGameState.getPacmanPosition()
    curFoodList = currentGameState.getFood().asList()
    curFoodCount = currentGameState.getNumFood()
    curGhostStates = currentGameState.getGhostStates()
    curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]
    curCapsules = currentGameState.getCapsules()
    curScore = currentGameState.getScore()

    foodLeft = 1.0/(curFoodCount + 1.0)
    ghostDist = float("INF")
    scaredGhosts = 0

    # print curScaredTimes

    for ghostState in curGhostStates:
      
      ghostPos = ghostState.getPosition()
      if curPos == ghostPos:
        return float("-INF")
      else:
        ghostDist = min(ghostDist,manhattanDistance(curPos,ghostPos))
      
      if ghostState.scaredTimer != 0:
        scaredGhosts += 1

    capDist = float("INF")
    for capsuleState in curCapsules:
      capDist = min(capDist,manhattanDistance(curPos,capsuleState))

    ghostDist = 1.0/(1.0 + (ghostDist/(len(curGhostStates))))
    capDist = 1.0/(1.0 + len(curCapsules))
    scaredGhosts = 1.0/(1.0 + scaredGhosts)


    return curScore + (foodLeft + ghostDist + capDist)

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

