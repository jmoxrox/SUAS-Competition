'''
Created on Jan 10, 2017

@author: phusisian
'''
#from ObjAvoid.Test import Test
from Mass import Mass
from Vector import Vector
from MultiDimPoint import MultiDimPoint
from graphics import *
from Window import Window
from NavVectorMaker import NavVectorMaker
from TestFunctions import TestFunctions

class DroneMass(Mass):
    DEFAULT_DRONE_MASS = 1

    def __init__(self, boundMassHolder, pointIn, massIn):
        Mass.__init__(self, boundMassHolder, pointIn, massIn)
        self.velocityVector = Vector.createEmptyVectorWithDim(len(self.getPoint()))
        randNavPoints = TestFunctions.getRandomPointsInBounds(2, 25, [(-350, 350), (-350, 350)])
        self.navVectorMaker = NavVectorMaker(self, randNavPoints)
        self.speed = 500
    '''currently masses can't have any forces of their own. set netVector to the force of the mass
    if I ever do ad it instead of (0,0,0)'''
    def getNetForceVector(self):
        netVector = Vector.createEmptyVectorWithDim(len(self.getPoint()))#Vector([0,0,0])
        for i in range(0, len(self.boundMassHolder)):
            if not self.boundMassHolder[i] == self:
                '''vector casted from that mass to this one, so force should be facing the correct direction.'''
                netVector += self.boundMassHolder[i].getForceVectorToMass(self)
        return netVector

    def applyMotions(self):
        self.navVectorMaker.setVelocityVectorToNextTravelPoint(self.speed)
        self.applyForce(self.getNetForceVector())
        self.applyVelocity()

    def applyForce(self, force):
        #(1/2) at^2
        self.point += (force*(1.0/float(self.mass)))*(Window.REFRESH_TIME**2)*0.5

    def applyVelocity(self):
        #print("Velocity Vector: " + str(self.velocityVector))
        self.point += self.velocityVector*Window.REFRESH_TIME

    def draw(self, win):
        self.point.draw(win, "red")
        #self.navVectorMaker.draw(win)
        #c = Circle(Point(int(self.point[0] + win.getCenterPoint()[0]), int(win.getCenterPoint()[1] - self.point[1])), 2)#subtracted so reversed y axis graphics work.
        #c.setFill("red")
        #c.draw(win.getGraphWin())

    def getNavVectorMaker(self):
        return self.navVectorMaker

    def setSpeed(self, speedIn):
        self.speed = speedIn

    def getSpeed(self):
        return self.speed

    def setVelocityVector(self, vectorIn):
        self.velocityVector = vectorIn

    def getVelocityVector(self):
        return self.velocityVector

    def __repr__(self):
        returnString = "Drone Mass "
        returnString += Mass.__repr__(self)
        return returnString