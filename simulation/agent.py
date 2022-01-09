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
        self.recoveredSince = None

    def move(self,direction,xDimension,yDimension):
        """
        Moves the Agent by the given direction, within given dimensions

        :param direction: Object with x and y values, which take values between 0 and 1
        :param xDimension: The X-Dimension in which Agents can move
        :param yDimension: The Y-Dimension in which Agents can move
        """
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
        """
        Infect the Agents nearby the Agent

        :param agentList: The Collection of all Agents in the Simulation
        """

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
        """
        Increase the TimeCounter of an Agent beeing infected
        """
        self.TimeBeeingInfected +=1

    def setVirus(self,v):
        """
        Set a Virus to the agent
        """
        self.Virus = v

    def getInfected(self):
        """
        Change the State of an Agent of beeing Infectious
        """
        self.isInfected = True
        self.isSusceptible = False
        
    def getRemoved(self):
        """
        Change the State of an Agent of beeing Removed (Recovered)
        """
        self.isRemoved = True
        self.isInfected = False
        self.Virus = None
        self.TimeBeeingInfected = 0
        self.recoveredSince = 1

    def getDead(self):
        """
        Change the State of an Agent of beeing Dead 
        """
        self.isDead = True
        self.isInfected = False
        self.Virus = None
        self.TimeBeeingInfected = 0

    def returnToSusceptible(self, returnToSusceptible):
        """
        Returns Agents back to beeing Susceptible after x- Days.
        :var returnToSusceptible, int, Days after which Agent is susceptible again
        :return: void
        """

        if self.recoveredSince >= returnToSusceptible*25:
            self.isSusceptible = True

        self.recoveredSince += 1

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y