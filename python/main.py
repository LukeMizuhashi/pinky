import logging
from nodes import *

def netFunction():
    print("Foo")

def activationFunction():
    print("Bar")

result = {}

inputA = InputNode("inputA")
inputB = InputNode("inputB")

hiddenNode1 = HiddenNode(netFunction,activationFunction,"hidden1")
hiddenNode2 = HiddenNode(netFunction,activationFunction,"hidden2")

outputA = OutputNode(netFunction,activationFunction,result,"outputA")
outputB = OutputNode(netFunction,activationFunction,result,"outputB")

edgeFactory = EdgeFactory()
edgeFactory.makeDirectedEdge(inputA,hiddenNode1)
edgeFactory.makeDirectedEdge(inputA,hiddenNode2)
edgeFactory.makeDirectedEdge(inputB,hiddenNode1)
edgeFactory.makeDirectedEdge(inputB,hiddenNode2)

edgeFactory.makeDirectedEdge(hiddenNode1,outputA)
edgeFactory.makeDirectedEdge(hiddenNode1,outputB)
edgeFactory.makeDirectedEdge(hiddenNode2,outputA)
edgeFactory.makeDirectedEdge(hiddenNode2,outputB)

truthTable = [
    [0,0,0],
    [0,1,1],
    [1,0,1],
    [1,1,0]
]

for row in truthTable:
    logging.debug("New Row")
    inputA.sense(row[0])
    inputB.sense(row[1])

