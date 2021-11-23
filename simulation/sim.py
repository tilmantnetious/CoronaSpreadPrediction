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
        self.Environment = ruleset['env'][0]     #todo --> dynamisch ausbauen
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
                agList.append(ag(i, position(xPos, yPos), True, False, False))
            elif self.stateList[i] == "i":
                agList.append(ag(i, position(xPos, yPos), False, True, False))
            elif self.stateList[i] == "r":
                agList.append(ag(i, position(xPos, yPos), False, False, True))
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

    # Uodate die Farbe der Agenten
    def __updateColors(self):
        for i in range(self.Environment.populationAmmount):
            if (self.stateList[i] == "s"):
                self.colorList[i] = "blue"
            elif (self.stateList[i] == "i"):
                self.colorList[i] = "red"
            elif (self.stateList[i] == "r"):
                self.colorList[i] = "green"

    # Erfasse die GruppenGrößen
    def __getSIRAmmounts(self):
        sus, inf, rem = 0, 0, 0
        for a in self.agentList:
            if (a.isSusceptible == True):
                sus += 1
            elif (a.isInfected == True):
                inf += 1
            elif (a.isRemoved == True):
                rem += 1

        self.SusAmmountList.append(sus)
        self.InfAmmountList.append(inf)
        self.RemAmmountList.append(rem)

    # Starte Simulation
    def start(self, FPS):
        print("Start")
        iv = 1000 / FPS

        # erstelle 2 Plots
        fig, (ax1, ax2) = plt.subplots(1, 2)
        # Scatter Plot - Simulation
        sc = ax1.scatter(self.xCoordinates, self.yCoordinates, color=self.colorList)
        # Line Plot - Verbreitung
        pl1, = ax2.plot(self.TimeList, self.SusAmmountList, "-b", label="susceptible")
        pl2, = ax2.plot(self.TimeList, self.InfAmmountList, "-r", label="infectious")
        pl3, = ax2.plot(self.TimeList, self.RemAmmountList, "-g", label="removed")
        ax2.legend(loc="upper left")
        # Scatter Plot Spezifikationen
        ax1.set_xlim(0, self.Environment.xDimension)
        ax1.set_ylim(0, self.Environment.yDimension)
        ax1.set_xlabel("Position X")
        ax1.set_ylabel("Position Y")
        ax1.set_title(str(self.Environment.name) + " Simulation")
        # Line Plot Spezifikationen
        ax2.set_ylim(0, self.Environment.populationAmmount)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Agents")
        ax2.set_title(str(self.Environment.name) + " Spread")

        def animate(i):
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
                        self.agentList[i].getRemoved()
                elif (self.agentList[i].isRemoved == True):
                    pass

            # update die Koordinaten, Status und Farben der Agenten
            self.__updateCoordinates()

            # Hier der Spaß funkioniert noch nicht so gut
            self.__updateStates()
            self.__updateColors()

            # wenn 1 Sekunde vergangen ist, dann speichere den Zeitpunkt t in TimeList
            # und die Anzahl der S, I und R zum Zeitpunkt t
            self.__getSIRAmmounts()
            self.TimeList.append(self.TimeCounter / FPS)

            # erhöhe den Zeitpunktcounter um 1
            self.TimeCounter += 1

            # Update die Daten der Simualtion (Koordinaten der Agenten)
            sc.set_offsets(np.c_[self.xCoordinates, self.yCoordinates])
            sc.set_facecolor(self.colorList)

            # Update die Daten der Verbreitung (Kennzahlen der Gruppen)
            pl1.set_data(self.TimeList, self.SusAmmountList)
            pl2.set_data(self.TimeList, self.InfAmmountList)
            pl3.set_data(self.TimeList, self.RemAmmountList)
            # Update die x Achse des Line Plots
            ax2.relim()
            ax2.autoscale_view()

        self.ani = matplotlib.animation.FuncAnimation(fig, animate, frames=FPS * self.duration, interval=iv,
                                                 repeat=self.extinctDiseas)
        plt.show()

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
        elif (k == "extinctDiseas"):
            self.extinctDiseas = v