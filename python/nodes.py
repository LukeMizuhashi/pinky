import logging
import pdb
import uuid

logging.basicConfig(level=logging.DEBUG)

class Parent():

    def __init__(self,weight=None):
        self.weight = weight
        self.value = None
        # TODO Implement dropout feature using this switch
        # self.dropped = False

    def resetValue(self):
        self.value = None

    def setValue(self,value):
        self.value = value

    def setWeight(self,weight):
        self.weight = weight

    def getValue(self):
        return self.value

    def getWeight(self):
        return self.weight


class Pulse():

    def __init__(self,caller,value):
        self.uuid = uuid.uuid4().int
        self.caller = caller
        self.value = value


class Weight():

    def __init__(self,parent,value):
        self.uuid = uuid.uuid4().int
        self.parent = parent
        self.value = value


class Node():

    def __init__(self,netFunction,activationFunction,name=None):
        self.uuid = uuid.uuid4().int
        self.name = name
        self.parents = {}
        self.children = {}
        self.netFunction = netFunction
        self.activationFunction = activationFunction

    def addParent(self,parent,weight=None):
        if parent.uuid in self.parents:
            raise Exception("Parent already connected to this node")
        self.parents[parent.uuid] = Parent(weight)

    def setParentValue(self,pulse):
        if pulse.caller not in self.parents:
            raise Exception("Unknown caller sent pulse to hidden node")
        self.parents[pulse.caller].setValue(pulse.value)

    def setParentWeight(self,weight):
        if weight.parent not in self.parents:
            raise Exception("Attempted to set weight for unknown parent")
        self.parents[weight.parent].setWeight(weight.value)

    def allParentsCalled(self):
        allParentsCalled = True
        for parentId in self.parents:
            if self.parents[parentId].getValue() != None:
                allParentsCalled = False
                break
        return allParentsCalled

    def resetParents(self):
        for parentId in self.parents:
            self.parents[parentId].reset()

    def addChild(self,child):
        if child.uuid in self.children:
            raise Exception("Child already connected to this node")
        self.children[child.uuid] = child


class InputNode(Node):

    def __init__(self,name=None):
        Node.__init__(self,None,None,name)

    def sense(self,value):
        logging.debug(self.name + " sensing " + str(value))
        pulse = Pulse(self.uuid,value)
        for child in self.children:
            self.children[child].sense(pulse)


class HiddenNode(Node):

    def __init__(self,netFunction,activationFunction,name=None):
        Node.__init__(self,netFunction,activationFunction,name)

    def sense(self,pulse):
        logging.debug(self.name + " sensing " + str(pulse.value))
        pdb.set_trace()
        self.setParentValue(pulse)
        if self.allParentsCalled():
            netOut = self.netFunction(self.parents)
            activationOut = self.activationFunction(netOut)
            pulse = Pulse(self.uuid,activationOut)
            for child in self.children:
                child.sense(pulse)
            

class OutputNode(Node):

    def __init__(self,netFunction,activationFunction,collector,name=None):
        Node.__init__(self,netFunction,activationFunction,name)
        self.collector = collector
        self.name = name

    def sense(self,pulse):
        logging.debug(self.name + " sensing " + str(pulse.value))
        self.setParentValue(pulse)
        if self.allParentsCalled():
            netOut = self.netFunction(self.parents)
            activationOut = self.activationFunction(netOut)
            self.collector[self.uuid] = activationOut


class EdgeFactory():

    def makeDirectedEdge(self,source,destination):
        source.addChild(destination)
        destination.addParent(source)


