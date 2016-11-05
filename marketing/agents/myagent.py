# You will implement this class
# At the minimum, you need to implement the selectNodes function
# If you override __init__ from the agent superclass, make sure that the interface remains identical as in agent; 
# otherwise your agent will fail

from agent import Agent

from collections import deque
import copy
from sets import Set

class Frontier:
    
    def __init__(self):
        self.nodes = deque()

    def pop(self):
        return self.nodes.popleft()

    def pushback(self, x):
        self.nodes.append(x)

    def pushbacklist(self, xlist):
        for x in xlist:
            self.pushback(x)

    def pushfront(self, x):
        self.nodes.appendleft(x)

    def pushfrontlist(self, xlist):
        for x in xlist:
            self.pushfront(x)

    def empty(self):
        return not self.nodes

class MyAgent(Agent):
    def selectNodes(self, network):
        numNodes = network.size()

        selected = []

        # store the set of neighbors for each node
        nodeNeighbors = []
        for i in range(numNodes):
            nbrs = Set(network.getNeighbors(i))
            nbrs.add(i)
            nodeNeighbors.append(nbrs)

        # initialize the "Frontier"
        frontier = Frontier()

        # initialize selected nodes
        x = []

        for i in range(numNodes):
            x.append(0)

        best = tuple(x)
        bestVal = 0

        ### your code goes here ###
        # [ NOTE: fill in where necessary ]
        minDegree = network.maxDegree()

        for i in range(numNodes):
            if network.degree(i) < minDegree:
                minDegree = network.degree(i)

        frontier.pushback(x)

        count = 0
        while not frontier.empty():

            # take the front element from the frontier
            x = frontier.pop()

            estBestVal = 0


            minimum = []
            maximum = []

            searchDepth = 0

            totalNeighbors = []
            for i in range(len(x)):
                if x[i] == 1:
                    estBestVal -= 1
                    # searchDepth += 1
                    neighbors = network.getNeighbors(i)
                    for node in neighbors:
                        if node not in totalNeighbors:
                            totalNeighbors.append(node)

            estBestVal += len(totalNeighbors)

            for i in range(len(x)):
                if x[i] == 0:
                    numNeighborsOfX = network.degree(i)
                    minimum.append(estBestVal + self.budget)
                    maximum.append(estBestVal + numNeighborsOfX - self.budget)

                else:
                    minimum.append(0)
                    maximum.append(estBestVal+1)

            for i in range(len(maximum)):
                if x[i]!=2:
                    for j in range(len(maximum)):
                        if x[j]==1:
                            if (maximum[i] <= minimum[j] or maximum[i] <= estBestVal):
                                x[i] = 2

            count += 1

            print count

            childList = self.expand(x)
            if (childList != []):
                frontier.pushbacklist(childList)
            else:
                totalNeighbors = []
                for i in range(len(x)):
                    if x[i] == 1:
                        neighbors = network.getNeighbors(i)
                        for node in neighbors:
                            if node not in totalNeighbors:
                                totalNeighbors.append(node)

                if (bestVal < len(totalNeighbors)):
                    bestVal = len(totalNeighbors)
                    best = tuple(x)
                    ### end your code ###

        for i in range(numNodes):
            if (best[i] == 1):
                selected.append(i)
        return selected


    def expand(self, x):
        """
        expand a node in the tree

        returns children of this node in the search tree
        """

        nodes = []
        newx=[]
        ### your code goes here  ####
        budgetUsed = 0
        for node in x:
            if (node == 1):
                budgetUsed += 1

        if (budgetUsed < self.budget):
            for i in range(len(x)):
                if x[i] == 0:
                    newX = x[:]
                    newX[i] = 1
                    print newX
                    nodes.append(newX)

        ### end your code  ##
        return nodes


    def eval(self, nodeNeighbors, x):
        """
        evaluate the value of node x
        nodeNeighbors is an auxiliary data structure
        keeping track of sets of neighbors for each node
        """

        nbrs = Set()
        for i in range(len(x)):
            if x[i] == 1:
                for j in nodeNeighbors[i]:
                    nbrs.add(j)

        return len(nbrs)

    def display():
        print "Agent ID ", self.id

