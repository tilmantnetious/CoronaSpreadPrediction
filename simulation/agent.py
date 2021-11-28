"""
Agent Class

@author David Hammbartsumjan
@author Tilman Schlichting
@since 10.11.2021
@copyright CC BY-SA

"""
import random

class Agent:
    def __init__(self, id, position, isSusceptible, isInfected, isRemoved, isDead):
        self.id = id
        self.position = position
        self.isSusceptible = isSusceptible
        self.isInfected = isInfected
        self.isRemoved = isRemoved
        self.isDead = isDead
        self.Virus = None
        self.TimeBeeingInfected = 0

    def move(self,direction,xDimension,yDimension):
        if self.position.x+direction.x>xDimension:
            direction.x = direction.x*(-1)
        elif self.position.x+direction.x<0:
            direction.x = direction.x*(-1)

        if self.position.y+direction.y>yDimension:
            direction.y = direction.y*(-1)
        elif self.position.y+direction.y<0:
            direction.y = direction.y*(-1)

        self.position.x += direction.x
        self.position.y += direction.y
    
    def infect(self, agentList):
        #Quadrat der Hypothenuse
        sh = self.Virus.infectionRadius**2

        #checke als erstes welche Punkte in Betracht kommen könnten
        for i in agentList:
            #Summe der Kathetenquadrate
            ssk = abs(i.position.x-self.position.x)**2 + abs(i.position.y-self.position.y)**2
            #Wenn die SSK <= SH ist, dann befindet sich der Punkt im Infektionsradius und es kann eine mögliche Infektion stattfinden
            if (ssk<=sh) and i.isSusceptible == True:
                #Ziehe zufallszahl r
                #Ist diese größer, als die Infektionswahrscheinlichkeit, infiziere
                r = random.random()
                if r>1-self.Virus.infectionProbability:
                    i.getInfected()

    def increaseTimeBeeingInfected(self):
        self.TimeBeeingInfected +=1

    def setVirus(self,v):
        self.Virus = v

    def getInfected(self):
        self.isInfected = True
        self.isSusceptible = False
        
    def getRemoved(self):
        self.isRemoved = True
        self.isInfected = False
        self.Virus = None
        self.TimeBeeingInfected = 0

    def getDead(self):
        self.isDead = True
        self.isInfected = False
        self.Virus = None
        self.TimeBeeingInfected = 0

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y