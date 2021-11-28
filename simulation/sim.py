"""
Simulation Module

@author David Hammbartsumjan
@author Tilman Schlichting
@since 27.10.2021
@copyright CC BY-SA

"""
#import matplotlib; matplotlib.use("Qt5Agg") #use on qt-based window-renderer
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import math
import random

from .agent import Agent as ag
from .agent import Position as position

class Sim:
    def __init__(self, ruleset):
        self.Virus = ruleset['virus'][0]         #todo --> dynamisch ausbauen!
        self.Environment = ruleset['env'][0]     #todo --> dynamisch ausbauen!
        self.stateList = self.__setStates()
        self.colorList = self.__setColors()
        self.agentList = self.__generateAgents()
        self.xCoordinates, self.yCoordinates = self.__setCoordinates()
        self.direction = self.__setDirections()
        self.duration = 1
        self.extinctDiseas = False
        self.SusAmmountList = []
        self.InfAmmountList = []
        self.RemAmmountList = []
        self.DeaAmmountList = []
        self.TimeList = []
        self.TimeCounter = 0
        self.ani = False

    # generiere Agenten mittels der Populationsanzahl der Enviornment
    def __generateAgents(self):
        agList = []
        for i in range(self.Environment.populationAmmount):
            xPos = random.random() * self.Environment.xDimension
            yPos = random.random() * self.Environment.yDimension
            if self.stateList[i] == "s":
                agList.append(ag(i, position(xPos, yPos), True, False, False, False))
            elif self.stateList[i] == "i":
                agList.append(ag(i, position(xPos, yPos), False, True, False, False))
            elif self.stateList[i] == "r":
                agList.append(ag(i, position(xPos, yPos), False, False, True, False))
            elif self.stateList[i] == "d":
                agList.append(ag(i, position(xPos, yPos), False, False, False, True))

        return agList

    # Setze die Koordinaten der Agenten in einen x- und y- Array fest
    def __setCoordinates(self):
        xCoor = []
        yCoor = []
        for i in range(self.Environment.populationAmmount):
            xCoor.append(self.agentList[i].position.x)
            yCoor.append(self.agentList[i].position.y)
        return xCoor, yCoor

    # Update die Koordianten der Agenten
    def __updateCoordinates(self):
        for i in range(self.Environment.populationAmmount):
            self.xCoordinates[i] = self.agentList[i].position.x
            self.yCoordinates[i] = self.agentList[i].position.y

    # Weise den Agente eine Richtung zu, welche in einem Array gespeichert wird
    def __setDirections(self):
        dir = []
        for i in range(self.Environment.populationAmmount):
            a = random.random() * 2 * math.pi
            b = random.random() * 2 * math.pi
            dir.append(position((math.sin(a)) / 10, (math.cos(b)) / 10, ))
        return dir

    # Weise jedem Agenten den Susceptiblestatus zu und einem den infected Status
    def __setStates(self):
        states = []
        infect = int(random.random() * self.Environment.populationAmmount)
        for i in range(self.Environment.populationAmmount):
            if (i == infect):
                states.append("i")
            else:
                states.append("s")
        return states

    # Weise jedem Agenten entsprechend seines Status eine Farbe zu
    def __setColors(self):
        colors = []
        for i in range(self.Environment.populationAmmount):
            if (self.stateList[i] == "s"):
                colors.append("blue")
            elif (self.stateList[i] == "i"):
                colors.append("red")
            elif (self.stateList[i] == "r"):
                colors.append("green")
            elif (self.stateList[i] == "d"):
                colors.append("grey")
        return colors

    # Update den Status der Agenten
    def __updateStates(self):
        for i in range(self.Environment.populationAmmount):
            if (self.agentList[i].isSusceptible == True):
                self.stateList[i] = "s"
            elif (self.agentList[i].isInfected == True):
                self.stateList[i] = "i"
            elif (self.agentList[i].isRemoved == True):
                self.stateList[i] = "r"
            elif (self.agentList[i].isDead == True):
                self.stateList[i] = "d"

    # Uodate die Farbe der Agenten
    def __updateColors(self):
        for i in range(self.Environment.populationAmmount):
            if (self.stateList[i] == "s"):
                self.colorList[i] = "blue"
            elif (self.stateList[i] == "i"):
                self.colorList[i] = "red"
            elif (self.stateList[i] == "r"):
                self.colorList[i] = "green"
            elif (self.stateList[i] == "d"):
                self.colorList[i] = "grey"

    # Erfasse die GruppenGrößen
    def __getSIRAmmounts(self):
        sus, inf, rem , dea = 0, 0, 0, 0
        for a in self.agentList:
            if (a.isSusceptible == True):
                sus += 1
            elif (a.isInfected == True):
                inf += 1
            elif (a.isRemoved == True):
                rem += 1
            elif (a.isDead == True):
                dea += 1

        self.SusAmmountList.append(sus)
        self.InfAmmountList.append(inf)
        self.RemAmmountList.append(rem)
        self.DeaAmmountList.append(dea)

    # Starte Simulation
    def start(self, FPS):
        print("Start")
        duration = 0

        #Initialisierung des Returnarrays
        start_x_pos, start_y_pos =  self.__setCoordinates()
        return_x_pos = [start_x_pos]
        return_y_pos = [start_y_pos]
        return_color = [self.__setColors()]
        return_SusAmmountList = []
        return_InfAmmountList = []
        return_RemAmmountList = []
        return_DeaAmmountList = []
        return_timeList = []

        while duration <= self.duration * FPS:

            # Bewege jeden einzelnen Agenten
            for i in range(self.Environment.populationAmmount):
                self.agentList[i].move(self.direction[i], self.Environment.xDimension, self.Environment.yDimension)

            # checke den Status jedes Agenten und führe die dazugehörige Operation aus.
            for i in range(self.Environment.populationAmmount):
                if (self.agentList[i].isSusceptible == True):
                    pass
                elif (self.agentList[i].isInfected == True):
                    # Weise dem infizierten den Virus zu
                    self.agentList[i].setVirus(self.Virus)
                    # infiziere sein Umfeld
                    self.agentList[i].infect(self.agentList)
                    # erhöhe die Zeit, in der der Agent infizeirt ist
                    self.agentList[i].increaseTimeBeeingInfected()
                    # Ist die INfektionszeit = der INfektionszeit des Virus, entferne den Agenten
                    if (self.agentList[i].TimeBeeingInfected == self.Virus.infectionTime * FPS):
                        r = random.random()
                        if(r<self.Virus.mortalityRate):
                            self.agentList[i].getDead()
                            self.direction[i].x = 0
                            self.direction[i].y = 0
                        else:
                            self.agentList[i].getRemoved()
                elif (self.agentList[i].isRemoved == True):
                    pass

            # update die Koordinaten, Status und Farben der Agenten
            self.__updateCoordinates()
            return_x_pos.append(self.xCoordinates.copy())
            return_y_pos.append(self.yCoordinates.copy())

            # Update den Status und die Farbe der Agenten
            self.__updateStates()
            self.__updateColors()
            return_color.append(self.colorList.copy())

            # wenn 1 Sekunde vergangen ist, dann speichere den Zeitpunkt t in TimeList
            # und die Anzahl der S, I und R zum Zeitpunkt t
            self.__getSIRAmmounts()
            return_SusAmmountList.append(self.SusAmmountList.copy())
            return_InfAmmountList.append(self.InfAmmountList.copy())
            return_RemAmmountList.append(self.RemAmmountList.copy())
            return_DeaAmmountList.append(self.DeaAmmountList.copy())

            self.TimeList.append(self.TimeCounter / FPS)
            return_timeList.append(self.TimeList.copy())

            # erhöhe den Zeitpunktcounter um 1
            self.TimeCounter += 1

            #Laufvariable
            duration += 1


        return {
            "frame" : {
                "x_pos" : return_x_pos,
                "y_pos" : return_y_pos,
                "color" : return_color,
                "x_lim" : self.Environment.xDimension,
                "y_lim" : self.Environment.yDimension,
                "env_name" : self.Environment.name,
                "pop_amount" : self.Environment.populationAmmount,
            },
            "movement" : {
                "SusAmmountList" : return_SusAmmountList,
                "InfAmmountList" : return_InfAmmountList,
                "RemAmmountList" : return_RemAmmountList,
                "DeaAmmountList" : return_DeaAmmountList,
                # "SusAmmountList": self.SusAmmountList,
                # "InfAmmountList": self.InfAmmountList,
                # "RemAmmountList": self.RemAmmountList,
                "timeList" : return_timeList,
                "colorList" : return_color
            }
        }


    # Setze StoppBedingung der Simulation
    # (duration -int =Dauer der Simulation in Sekunden, extinctDiseas -Bool =standardmäßig False, wenn true, hört die Simulation auf, wenn die Krankheit ausgestorben ist)
    def setStopCondition(self, **conditions):
        keys = []
        vals = []
        for k, v in conditions.items():
            keys.append(k)
            vals.append(v)

        if (k == "duration"):
            self.duration = v
        elif (k == "extinctDisease"):
            self.extinctDiseas = v